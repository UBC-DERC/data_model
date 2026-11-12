"""Testing the construction of the ddlml object, and the use of the info_dict class"""

from ddlml.object_classes import contact_dict, ddlml_info, license_dict


def test_info_bloc_creation_licenseId():
    license = license_dict(
        full_name="MIT License",
        licenseId="MIT",
    )
    contact1 = contact_dict(
        name="John Doe",
        email="john.doe@example.com",
        url="https://example.com/john.doe",
    )
    info = ddlml_info(
        version="1.0.0",
        title="Dairy Model",
        summary="A simple dairy model",
        license=license,
        contacts=[contact1],
    )
    assert info.version == "1.0.0"
    assert info.title == "Dairy Model"
    assert info.summary == "A simple dairy model"
    assert info.license == license
    assert info.contacts == [contact1]


def test_info_bloc_creation_licenseUrl():
    license = license_dict(
        full_name="MIT License",
        url="https://opensource.org/licenses/MIT",
    )
    contact1 = contact_dict(
        name="John Doe",
        email="john.doe@example.com",
        url="https://example.com/john.doe",
    )
    info = ddlml_info(
        version="1.0.0",
        title="Dairy Model",
        summary="A simple dairy model",
        license=license,
        contacts=[contact1],
    )
    assert info.version == "1.0.0"
    assert info.title == "Dairy Model"
    assert info.summary == "A simple dairy model"
    assert info.license == license
    assert info.contacts == [contact1]

def test_contact_dict_creation():
    contact = contact_dict(
        name="Alpha Beta",
        email="jonobono@example.com",
        url="https://example.com/robotcity",
    )
    assert contact.name == "Alpha Beta"
    assert contact.email == "jonobono@example.com"
    assert contact.url == "https://example.com/robotcity"

def test_contact_dict_creation_missing_email():
    contact = contact_dict(
        name="Jane Smith",
        url="https://example.com/jane.smith",
    )
    assert contact.name == "Jane Smith"
    assert contact.email is None
    assert contact.url == "https://example.com/jane.smith"
