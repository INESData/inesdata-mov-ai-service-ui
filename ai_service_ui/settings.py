import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    resources_path: str = "resources"

    styles:str = os.path.join(resources_path, "style.css")
    gmv_logo:str = os.path.join(resources_path, "gmv_logo.svg")

    stop_information_path:str = os.path.join(resources_path, "stop_information.json")
    line_information_path:str = os.path.join(resources_path, "line_information.json")

    line_list:list = ['-','27','42', '49', '67', '70', '107', '129', '134', '135', '173', '174', '175', '176', '177', '178']
    stop_list: list = ['-','29', '30', '33', '35', '37', '39', '42', '44', '47', '50', '52', '54', '56', '60', '62', '65', '66', '72', '78', '82', '85', '86', '87', '88', '89', '126', '128', '130', '132', '134', '136', '138', '140', '145', '146', '203', '205', '207', '208', '210', '212', '214', '215', '218', '220', '222', '224', '226', '228', '230', '232', '234', '236', '240', '242', '244', '246', '250', '253', '269', '271', '399', '402', '497', '499', '501', '503', '509', '510', '1021', '1022', '1025', '1357', '1360', '1364', '1366', '1368', '1374', '1376', '1377', '1487', '1488', '1489', '1494', '1496', '1498', '1500', '1501', '1503', '1505', '1507', '1509', '1511', '1515', '1517', '1530', '1532', '1537', '1542', '1544', '1546', '1548', '1550', '1552', '1554', '1556', '1558', '1602', '1604', '1606', '1608', '1610', '1612', '1615', '1617', '1619', '1621', '1623', '1625', '1627', '1629', '1631', '1633', '1732', '1734', '1736', '1739', '1741', '1743', '1745', '1749', '1751', '1753', '1760', '1762', '1837', '1839', '1841', '1843', '1845', '1846', '1848', '1850', '1851', '1852', '1866', '2148', '2150', '2653', '2864', '2968', '2970', '3245', '3247', '3249', '3252', '3253', '3254', '3256', '3258', '3260', '3261', '3267', '3269', '3270', '3272', '3279', '3544', '3566', '3568', '3578', '3580', '3594', '3603', '3605', '3620', '3621', '3623', '3634', '3664', '3670', '3671', '3683', '3733', '3769', '3771', '3778', '3790', '3794', '3796', '3821', '3822', '3823', '3826', '3869', '3870', '3872', '3874', '3918', '4033', '4230', '4264', '4266', '4268', '4273', '4354', '4366', '4382', '4493', '4495', '4501', '4502', '4508', '4651', '4708', '4731', '4732', '4734', '4736', '4741', '4752', '4777', '4968', '5016', '5018', '5020', '5133', '5267', '5329', '5333', '5337', '5395', '5397', '5399', '5443', '5458', '5511', '5517', '5518', '5602', '5603', '5604', '5605', '5606', '5607', '5608', '5609', '5610', '5611', '5612', '5632', '5633', '5634', '5635', '5636', '5722', '5747', '5798', '5799', '5800', '5801', '5802', '5803', '5804', '5805', '5806', '5807', '5887', '5892', '5894', '5899', '5911', '5915', '5917', '5919', '5921', '5926', '5927', '5982', '5984', '5996', '51022', '51023']
    lines_per_stop_path:str = os.path.join(resources_path, "lines_per_stop.json")
    stop_per_lines:str = os.path.join(resources_path, "stop_per_line.json")

    # Data space components
    api_key: str = "e54d4431-5dab-474e-b71a-0db1fcb9e659"

    auth_url: str = "https://auth.ds.inesdata-project.eu/realms/mobility/protocol/openid-connect/token"
    keycloak_base_url: str = "https://auth.ds.inesdata-project.eu/realms/mobility"

    license_api_url: str = "https://conn-gmv-mobility.ds.inesdata-project.eu/public/"
    prediction_api_url: str =  "https://conn-gmv-mobility.ds.inesdata-project.eu/public/{stop_id}/arrives/{line_id}"

    redirect_uri: str = "http://localhost:8501"

    start_transfer_url: str = "https://conn-ses-mobility.ds.inesdata-project.eu/management/v3/transferprocesses"
    get_transfer_url: str = "https://conn-ses-mobility.ds.inesdata-project.eu/management/v1/edrs/{transfer_id}/dataaddress"

    counter_party_address: str = "https://conn-gmv-mobility.ds.inesdata-project.eu/protocol"
    vocabulary: str = "https://w3id.org/edc/v0.0.1/ns/"

    connector_id:str = "conn-ses"
    contract_id_prediction:str = "eb02a4eb-e7fe-481f-9c49-6dca8d582f13"
    asset_id_prediction:str = "bus_arrival_prediction"
    contract_id_license:str = "68c03a2b-d0cd-476f-999f-a74aabaf646a"
    asset_id_license:str = "license"

    client_id: str = "dataspace-users"
    grant_type: str = "password"

    class Config:
        """Config."""

        env_file = ".env"

@lru_cache()
def get_settings():
    """Get settings."""
    return Settings()


settings = get_settings()
