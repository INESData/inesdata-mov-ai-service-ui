import argparse
import random
import re
from datetime import datetime

import pandas as pd
from example_cookiecutter.logger import logger as logging
from faker import Faker
from pandas import DataFrame

logger = logging.get_logger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # Parametro para el fichero de configuración del entorno
    parser.add_argument(
        "-orp", "--output_report_path", type=str, required=True
    )

    args = parser.parse_args()
    output_report_path = args.output_report_path

    fake = Faker()

    def generate_random_data() -> DataFrame:
        """Generate_random_data.

        Returns: DataFrame
        """
        d = {}
        date = "%d-%b-%Y (%H:%M:%S.%f)"

        # columns that use faker

        d["first_name"] = lambda: fake.first_name()
        d["last_name"] = lambda: fake.last_name()
        d["personal_email"] = (
            lambda: fake.email()
            if random.randint(0, 1) == 0
            else random.choice(
                ["nn@.com", 123123123, "nnn@aaa", "foo", "swing", None]
            )
        )
        d["ssn"] = lambda: fake.ssn()
        d["birth_date"] = (
            lambda: fake.date_between_dates(
                date_start=datetime(1960, 1, 1), date_end=datetime(2000, 1, 1)
            ).strftime(date)
            if random.randint(0, 1) == 0
            else None
        )
        d["start_date"] = (
            lambda: fake.date_between_dates(
                date_start=datetime(1995, 1, 1), date_end=datetime(2019, 1, 1)
            ).strftime(date)
            if random.randint(0, 1) == 0
            else None
        )

        d["office"] = lambda: fake.city()
        d["title"] = lambda: fake.job()

        # columns that do not use faker

        d["gender"] = lambda: "M" if random.randint(0, 1) == 0 else "F"
        d["org"] = lambda: random.choice(
            ["Engineer", "Sales", "Associate", "Manager", "VP", None]
        )
        d["accrued_holidays"] = (
            lambda: random.randint(0, 20)
            if random.randint(0, 1) == 0
            else random.randint(20, 100)
        )
        d["salary"] = (
            lambda: round(random.randint(90000, 120000) / 1000) * 1000
            if random.randint(0, 1) == 0
            else None
        )
        d["bonus"] = (
            lambda: round(random.randint(0, 5000) / 500) * 500
            if random.randint(0, 1) == 0
            else None
        )

        df = pd.DataFrame({k: [d[k]()] for k in d.keys()})

        for _ in range(200):
            df_row = pd.DataFrame({k: [d[k]()] for k in d.keys()})
            df = df.append(df_row)

        print(df.head())
        print(df.columns)
        return df

    data = generate_random_data()

    profile = data.profile_report(title="Pandas Profiling Report")
    profile.to_file(output_file=output_report_path)

    print(data.isnull().sum(axis=0))

    print(data.isnull().sum(axis=0) / data.shape[0] * 100)

    for col in data:
        print(
            "Valores unicos para la columna "
            + str(col)
            + ": "
            + str(len(data[col].unique()))
        )
        print(
            "Porcentaje de valores unicos para la columna "
            + str(col)
            + ": "
            + str(len(data[col].unique()) / data[col].count() * 100)
            + "%"
        )

    def check_email(x: str) -> bool:
        """Expresion regular para verificar correos.

        Args:
            x (str): valor

        Returns: bool
        """
        r = re.compile(
            r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:["
            r"a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$ "
        )
        is_email = False
        if x is not None and isinstance(x, str):
            is_email = bool(r.match(x))
        return is_email

    print(
        "Porcentaje de correos verdaderos : "
        + str(
            data["personal_email"].apply(lambda x: check_email(x)).sum()
            / data["personal_email"].shape[0]
            * 100
        )
        + "%"
    )

    upper_limit = 20
    lower_limit = 0

    def check_range(x: str) -> bool:
        """Check_range.

        Args:
            x (str): valor

        Returns: bool
        """
        is_in_range = False
        if isinstance(x, int) and (x > lower_limit and x < upper_limit):
            is_in_range = True
        return is_in_range

    print(
        "Porcentaje de valores correctos : "
        + str(
            data["accrued_holidays"].apply(lambda x: check_range(x)).sum()
            / data["accrued_holidays"].shape[0]
            * 100
        )
        + "%"
    )

    def check_date(x: str) -> bool:
        """Check_date.

        Args:
            x (str): valor

        Returns: bool
        """
        is_date = False
        if isinstance(x, str):
            try:
                is_date = True
            except Exception as e:
                logger.error(e)
                is_date = False
        return is_date

    print(
        "Porcentaje de fechas correctas : "
        + str(
            data["start_date"].apply(lambda x: check_date(x)).sum()
            / data["start_date"].shape[0]
            * 100
        )
        + "%"
    )
