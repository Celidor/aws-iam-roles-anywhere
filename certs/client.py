from cryptography import x509
from cryptography.x509 import load_pem_x509_certificate, load_pem_x509_csr, PolicyInformation, ObjectIdentifier
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes, serialization
import datetime

from certs.ca import generate_key, write_key_to_disk, write_cert_to_disk


def cert_signing_request(private_key, certificate_information):
    # get cert info
    country = certificate_information["country"]
    state = certificate_information["state"]
    locality = certificate_information["locality"]
    organization = certificate_information["organization"]
    common_name = certificate_information["common_name"]
    organization_unit_name = certificate_information["organization_unit_name"]

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organization_unit_name),
                    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                ]
            ),
        )
        .sign(private_key, hashes.SHA256())
    )

    return csr.public_bytes(serialization.Encoding.PEM)


def write_csr_to_disk(csr, filepath):
    """Write certificate signing request to disk"""
    with open(f"{filepath}.csr", "wb") as f:
        f.write(csr)


def sign_tls_certificate_request(csr, ca_cert, ca_key, lifetime):
    """Sign TLS certificate request"""

    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=lifetime))
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH, ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=False,
        )
        .add_extension(
            x509.CertificatePolicies([PolicyInformation(ObjectIdentifier("2.23.140.1.2.1"), None)]),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(
                ca=False,
                path_length=None,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)
        # Sign client certificate with CA private key
    ).sign(ca_key, hashes.SHA256())

    # Return client certificate in PEM format
    print(f"certificate serial number {cert.serial_number} issued for {cert.subject}")

    return cert.public_bytes(serialization.Encoding.PEM)


def create_client_cert(certificate_information, ca_file_path, client_file_path, lifetime):
    # Generate CA private key
    key = generate_key()

    # Write private key to disk - test purposes only
    # For production use, should be stored securely and passphrase used
    write_key_to_disk(key, f"{client_file_path}.key")

    # Generate CSR
    csr = cert_signing_request(key, certificate_information)

    # Write CSR to disk
    write_csr_to_disk(csr, f"{client_file_path}")

    # Read CA certificate from disk
    with open(f"{ca_file_path}.pem", "rb") as f:
        ca_cert = f.read()

    # Read CA private key from disk
    with open(f"{ca_file_path}.key", "rb") as f:
        ca_key = f.read()

    # Sign client certificate with CA private key
    cert = sign_tls_certificate_request(
        load_pem_x509_csr(csr), load_pem_x509_certificate(ca_cert), load_pem_private_key(ca_key, None), lifetime
    )

    # Write client certificate to disk
    write_cert_to_disk(cert, client_file_path)


def sign_macos_certificate_request(csr, ca_cert, ca_key, certificate_information, lifetime):
    """Sign MacOS certificate request"""

    # get cert info
    country = certificate_information["country"]
    state = certificate_information["state"]
    locality = certificate_information["locality"]
    organization = certificate_information["organization"]
    common_name = certificate_information["common_name"]
    organization_unit_name = certificate_information["organization_unit_name"]

    cert = (
        x509.CertificateBuilder()
        .subject_name(
            x509.Name(
                [
                    x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organization_unit_name),
                    x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                ]
            ),
        )
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=lifetime))
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH, ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=False,
        )
        .add_extension(
            x509.CertificatePolicies([PolicyInformation(ObjectIdentifier("2.23.140.1.2.1"), None)]),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(
                ca=False,
                path_length=None,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)
        # Sign client certificate with CA private key
    ).sign(ca_key, hashes.SHA256())

    # Return client certificate in PEM format
    print(f"certificate serial number {cert.serial_number} issued for {cert.subject}")

    return cert.public_bytes(serialization.Encoding.PEM)


def create_macos_cert_from_csr(certificate_information, ca_file_path, macos_file_path, lifetime):
    # Read CSR from disk
    with open(f"{macos_file_path}/CertificateSigningRequest.certSigningRequest", "rb") as f:
        csr = f.read()

    # Read CA certificate from disk
    with open(f"{ca_file_path}.pem", "rb") as f:
        ca_cert = f.read()

    # Read CA private key from disk
    with open(f"{ca_file_path}.key", "rb") as f:
        ca_key = f.read()

    # Sign client certificate with CA private key
    cert = sign_macos_certificate_request(
        load_pem_x509_csr(csr),
        load_pem_x509_certificate(ca_cert),
        load_pem_private_key(ca_key, None),
        certificate_information,
        lifetime,
    )

    # Write client certificate to disk
    write_cert_to_disk(cert, f"{macos_file_path}/macos-client")

    return load_pem_x509_certificate(cert)
