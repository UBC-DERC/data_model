"""Testing the construction of the ddaml object, and the use of the info_dict class"""

from data_model.object_classes import contact_dict, ddaml_info, license_dict


def test_info_bloc_creation():
    license = license_dict(
        full_name="MIT License",
        licenseId="MIT",
        url="https://opensource.org/licenses/MIT",
    )
    contact1 = contact_dict(
        name="John Doe",
        email="john.doe@example.com",
        url="https://example.com/john.doe",
    )
    info = ddaml_info(
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
