from certs.ca import cert_info, create_root_ca
from certs.client import create_client_cert, create_macos_cert_from_csr

ca_file_path = "crypto/ca/test-ca"  # path including filename, excluding extension
client_file_path = "crypto/client/test-client"  # path including filename, excluding extension
macos_file_path = "crypto/macos"  # path excluding filename and extension

country = "GB"  # Approved 2 letter country code
state = "England"
locality = "London"
organization = "Test Company"
organization_unit_name = "Cloud Security"  # only added to client certificate
ca_common_name = "Test Company Root CA"
ca_lifetime = 3650  # 10 years
client_common_name = "Test Client"
client_lifetime = 365  # 1 year
macos_common_name = "MacOS Client"

rebuild_ca = True  # Set to false to prevent recreation of CA
client_cert = True  # Set to false to prevent recreation of client certificate
macos_cert = False  # Set to true after client CSR has been created


# Create CA - test purposes only
# For a production CA, private key should be generated and stored in secure HSM
if rebuild_ca:
    ca_certificate_information = cert_info(country, state, locality, organization, ca_common_name)
    create_root_ca(ca_certificate_information, ca_file_path, ca_lifetime)

# Create client certificate
if client_cert:
    client_certificate_information = cert_info(country, state, locality, organization, client_common_name)
    client_certificate_information["organization_unit_name"] = organization_unit_name

    create_client_cert(client_certificate_information, ca_file_path, client_file_path, client_lifetime)

if macos_cert:
    # Create certificate for MacOS client from CSR created in KeyChain
    client_certificate_information = cert_info(country, state, locality, organization, macos_common_name)
    client_certificate_information["organization_unit_name"] = organization_unit_name

    macos_cert = create_macos_cert_from_csr(
        client_certificate_information, ca_file_path, macos_file_path, client_lifetime
    )
