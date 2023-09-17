from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime


def generate_key(key_length=4096):
    """Generate RSA key"""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_length,
    )


def write_key_to_disk(key, filepath):
    """Write RSA key to disk"""
    with open(filepath, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def cert_info(country, state, locality, organization, common_name):
    """Certificate information"""
    return {
        "country": country,
        "state": state,
        "locality": locality,
        "organization": organization,
        "common_name": common_name,
    }


def create_self_signed_ca(key, certificate_information, lifetime):
    """Create Self-Signed CA"""

    # get cert info
    country = certificate_information["country"]
    state = certificate_information["state"]
    locality = certificate_information["locality"]
    organization = certificate_information["organization"]
    common_name = certificate_information["common_name"]

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]
    )
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=lifetime))
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.BasicConstraints(
                ca=True,
                path_length=None,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()),
            critical=False
            # Sign our certificate with our private key
        )
        .sign(key, hashes.SHA256())
    )

    # Return CA certificate in PEM format
    return cert.public_bytes(serialization.Encoding.PEM)


def write_cert_to_disk(cert, filepath):
    """Write certificate to disk"""

    with open(f"{filepath}.pem", "wb") as f:
        f.write(cert)


def create_root_ca(certificate_information, ca_file_path, lifetime):
    # Generate CA private key - test purposes only
    # For a production CA, private key should be generated and stored in a secure HSM
    key = generate_key()

    # Write private key to disk - test purposes only
    # For a production CA, private key should be generated and stored in a secure HSM
    write_key_to_disk(key, f"{ca_file_path}.key")

    # Generate CA public key - test purposes only
    # For a production CA, private key should never be brought into memory outside secure HSM
    ca_cert = create_self_signed_ca(key, certificate_information, lifetime)

    # Write the CA certificate to disk in PEM format
    write_cert_to_disk(ca_cert, ca_file_path)
