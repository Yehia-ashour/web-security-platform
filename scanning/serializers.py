# scanning/serializers.py
from rest_framework import serializers
from .models import ScanProfile, Scan, Vulnerability
from urllib.parse import urlsplit, urlunsplit
import ipaddress
import socket


def normalize_and_validate_public_http_url(raw_url: str) -> str:
    """
    Validate and normalize a user-supplied target URL with strong SSRF protections.

    Rules enforced:
    - Only http/https schemes.
    - Normalize scheme/hostname; strip whitespace; remove default ports (80/443).
    - Block localhost/loopback and private/reserved/link-local/multicast/unspecified ranges.
    - Resolve hostname and validate ALL resolved IPs (mitigate DNS rebinding).
    - Optionally block IP-literal URLs (force domain-based targets).
    - No outbound HTTP requests are performed; DNS resolution only.
    """
    if not isinstance(raw_url, str):
        raise serializers.ValidationError("target_url must be a string.")

    # Trim whitespace
    raw_url = raw_url.strip()

    # Parse URL
    try:
        parts = urlsplit(raw_url)
    except Exception:
        raise serializers.ValidationError("Malformed URL.")

    scheme = (parts.scheme or "").lower()
    if scheme not in ("http", "https"):
        raise serializers.ValidationError("Only http and https schemes are allowed.")

    if not parts.netloc:
        raise serializers.ValidationError("URL must include a hostname.")

    hostname = parts.hostname  # already without brackets for IPv6
    if not hostname:
        raise serializers.ValidationError("URL must include a valid hostname.")

    hostname_lc = hostname.lower().rstrip(".")

    # Block localhost explicitly
    if hostname_lc == "localhost":
        raise serializers.ValidationError("Localhost targets are not allowed.")

    # Optional but preferred: block numeric IP literals entirely
    host_for_ip_check = hostname_lc
    try:
        # ip_address raises ValueError if not an IP literal
        ipaddress.ip_address(host_for_ip_check)
        raise serializers.ValidationError("IP address literals are not allowed; use a domain name.")
    except ValueError:
        pass  # Not an IP literal → proceed

    # DNS resolution (prevent DNS rebinding by validating ALL answers)
    try:
        addrinfo = socket.getaddrinfo(host_for_ip_check, None)
    except socket.gaierror:
        raise serializers.ValidationError("Hostname could not be resolved.")
    except Exception:
        raise serializers.ValidationError("DNS resolution failed.")

    if not addrinfo:
        raise serializers.ValidationError("Hostname did not resolve to any address.")

    blocked_reason = None
    for family, _, _, _, sockaddr in addrinfo:
        if family == socket.AF_INET:
            ip_str = sockaddr[0]
        elif family == socket.AF_INET6:
            ip_str = sockaddr[0]
        else:
            # Unknown family → reject to be safe
            blocked_reason = "Unrecognized address family."
            break

        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            blocked_reason = "Resolved to an invalid IP address."
            break

        # Enforce blocks (covers: 127.0.0.0/8, ::1, 10/8, 172.16/12, 192.168/16, 169.254/16,
        # 0.0.0.0/8 via reserved/unspecified, fc00::/7 (private), fe80::/10 (link-local), etc.)
        if ip_obj.is_loopback:
            blocked_reason = "Loopback addresses are not allowed."
            break
        if ip_obj.is_private:
            blocked_reason = "Private address ranges are not allowed."
            break
        if ip_obj.is_link_local:
            blocked_reason = "Link-local addresses are not allowed."
            break
        if ip_obj.is_reserved:
            blocked_reason = "Reserved address ranges are not allowed."
            break
        if ip_obj.is_unspecified:
            blocked_reason = "Unspecified addresses are not allowed."
            break
        if ip_obj.is_multicast:
            blocked_reason = "Multicast addresses are not allowed."
            break

    if blocked_reason:
        raise serializers.ValidationError(blocked_reason)

    # Normalize: scheme/host lowercase, remove default port, ensure consistent formatting
    port = parts.port
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    # Preserve userinfo if present (without modifying)
    userinfo = ""
    if parts.username:
        userinfo = parts.username
        if parts.password:
            userinfo += f":{parts.password}"
        userinfo += "@"

    netloc_host = hostname_lc
    if port:
        netloc_host = f"{netloc_host}:{port}"

    netloc = f"{userinfo}{netloc_host}"

    path = parts.path or "/"
    normalized = urlunsplit((scheme, netloc, path, parts.query, parts.fragment))
    return normalized 


class ScanProfileSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = ScanProfile
        fields = [
            'id',
            'name',
            'target_url',
            'created_by',
            'created_by_username',
            'created_at'
        ]
        read_only_fields = ['created_by', 'created_by_username']

    def validate_target_url(self, value):
        """
        Strong SSRF-safe validation and normalization for target_url.
        Applies on both create and update operations.
        """
        return normalize_and_validate_public_http_url(value)



class VulnerabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vulnerability
        fields = '__all__' 



class ScanSerializer(serializers.ModelSerializer):
    vulnerabilities = VulnerabilitySerializer(many=True, read_only=True)
    scheduled_by_username = serializers.CharField(source='scheduled_by.username', read_only=True)

    class Meta:
        model = Scan
        fields = [
            'id',
            'target_url',
            'status',
            'start_time',
            'end_time',
            'scheduled_by_username',
            'vulnerabilities',
        ]
        read_only_fields = ['start_time', 'end_time']

    def validate_target_url(self, value):
        return normalize_and_validate_public_http_url(value)
