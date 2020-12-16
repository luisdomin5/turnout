import csv
from io import StringIO
from typing import List, Tuple

from django.core.files.base import ContentFile
from django.db import connection
from django.template.defaultfilters import slugify
from django.utils.timezone import now

from common import enums
from storage.models import StorageItem

from .models import Report

ABSENTEE_FIELDS: List[Tuple[str, str]] = [
    ("uuid", "ID"),
    ("subscriber_name", "Subscriber"),
    ("created_at", "Time Started (UTC)"),
    ("first_name", "First Name"),
    ("middle_name", "Middle Name"),
    ("last_name", "Last Name"),
    ("suffix", "Suffix"),
    ("date_of_birth", "Date of Birth"),
    ("email", "Email"),
    ("phone", "Phone"),
    ("address1", "Address 1"),
    ("address2", "Address 2"),
    ("city", "City"),
    ("zipcode", "Zipcode"),
    ("state_id", "State"),
    ("mailing_address1", "Mailing Address 1"),
    ("mailing_address2", "Mailing Address 2"),
    ("mailing_city", "Mailing City"),
    ("mailing_state_id", "Mailing State"),
    ("mailing_zipcode", "Mailing Zipcode"),
    ("sms_opt_in", "VoteAmerica SMS Opt In"),
    ("sms_opt_in_subscriber", "Subscriber SMS Opt In"),
    ("finished", "Completed"),
    ("self_print", "PDF Emailed to Voter"),
    ("finished_external_service", "Redirected To State Website"),
    ("leo_message_sent", "PDF submitted to LEO"),
    ("total_downloads", "PDF Download Count"),
    ("forms_sent", "Total Forms Mailed With Return Envelopes"),
    ("source", "source"),
    ("utm_source", "utm_source"),
    ("utm_medium", "utm_medium"),
    ("utm_campaign", "utm_campaign"),
    ("utm_content", "utm_content"),
    ("utm_term", "utm_term"),
    ("embed_url", "Embed URL"),
    ("session_id", "Session ID"),
    ("referring_tool", "Referring Tool"),
    ("updated_at", "Updated At (UTC)"),
]

REGISTER_FIELDS: List[Tuple[str, str]] = [
    ("uuid", "ID"),
    ("subscriber_name", "Subscriber"),
    ("created_at", "Time Started (UTC)"),
    ("previous_title", "Previous Title"),
    ("previous_first_name", "Previous First Name"),
    ("previous_middle_name", "Previous Middle Name"),
    ("previous_last_name", "Previous Last Name"),
    ("previous_suffix", "Previous Suffix"),
    ("title", "Title"),
    ("first_name", "First Name"),
    ("middle_name", "Middle Name"),
    ("last_name", "Last Name"),
    ("suffix", "Suffix"),
    ("date_of_birth", "Date of Birth"),
    ("gender", "Gender"),
    ("race_ethnicity", "Race-Ethnicity"),
    ("us_citizen", "US Citizen"),
    ("party", "Party"),
    ("email", "Email"),
    ("phone", "Phone"),
    ("address1", "Address 1"),
    ("address2", "Address 2"),
    ("city", "City"),
    ("zipcode", "Zipcode"),
    ("state_id", "State"),
    ("previous_address1", "Previous Address 1"),
    ("previous_address2", "Previous Address 2"),
    ("previous_city", "Previous City"),
    ("previous_state_id", "Previous State"),
    ("previous_zipcode", "Previous Zipcode"),
    ("mailing_address1", "Mailing Address 1"),
    ("mailing_address2", "Mailing Address 2"),
    ("mailing_city", "Mailing City"),
    ("mailing_state_id", "Mailing State"),
    ("mailing_zipcode", "Mailing Zipcode"),
    ("sms_opt_in", "VoteAmerica SMS Opt In"),
    ("sms_opt_in_subscriber", "Subscriber SMS Opt In"),
    ("finished", "Completed"),
    ("self_print", "PDF Emailed to Voter"),
    ("finished_external_service", "Redirected To State Website"),
    ("leo_message_sent", "PDF Submitted to LEO"),
    ("total_downloads", "Total Self Print Downloads"),
    ("forms_sent", "Total Forms Mailed With Return Envelopes"),
    ("source", "source"),
    ("utm_source", "utm_source"),
    ("utm_medium", "utm_medium"),
    ("utm_campaign", "utm_campaign"),
    ("utm_content", "utm_content"),
    ("utm_term", "utm_term"),
    ("embed_url", "Embed URL"),
    ("session_id", "Session ID"),
    ("referring_tool", "Referring Tool"),
    ("updated_at", "Updated At (UTC)"),
]

VERIFIER_FIELDS: List[Tuple[str, str]] = [
    ("uuid", "ID"),
    ("subscriber_name", "Subscriber"),
    ("created_at", "Time Started (UTC)"),
    ("first_name", "First Name"),
    ("last_name", "Last Name"),
    ("date_of_birth", "Date of Birth"),
    ("email", "Email"),
    ("phone", "Phone"),
    ("address1", "Address 1"),
    ("address2", "Address 2"),
    ("city", "City"),
    ("zipcode", "Zipcode"),
    ("state_id", "State"),
    ("sms_opt_in", "VoteAmerica SMS Opt In"),
    ("sms_opt_in_subscriber", "Subscriber SMS Opt In"),
    ("registered", "Registered"),
    ("source", "source"),
    ("utm_source", "utm_source"),
    ("utm_medium", "utm_medium"),
    ("utm_campaign", "utm_campaign"),
    ("utm_content", "utm_content"),
    ("utm_term", "utm_term"),
    ("embed_url", "Embed URL"),
    ("session_id", "Session ID"),
    ("updated_at", "Updated At (UTC)"),
]

LOCATOR_FIELDS: List[Tuple[str, str]] = [
    ("uuid", "ID"),
    ("subscriber_name", "Subscriber"),
    ("created_at", "Time Started (UTC)"),
    ("unstructured_address", "Unstructured Address"),
    ("state_id", "State"),
    ("county", "County"),
    ("city", "City"),
    ("zipcode", "Zipcode"),
    ("precinct_code", "Precinct code"),
    ("source", "source"),
    ("utm_source", "utm_source"),
    ("utm_medium", "utm_medium"),
    ("utm_campaign", "utm_campaign"),
    ("utm_content", "utm_content"),
    ("utm_term", "utm_term"),
    ("embed_url", "Embed URL"),
    ("session_id", "Session ID"),
]


def generate_name(report: Report):
    if report.subscriber:
        filename = slugify(
            f'{now().strftime("%Y%m%d%H%M")}_{report.subscriber.slug}_{report.type.label}_export'
        ).lower()
    else:
        filename = slugify(
            f'{now().strftime("%Y%m%d%H%M")}_fullprogram_{report.type.label}_export'
        )
    return f"{filename}.csv"


def report_runner(report: Report):
    if report.type == enums.ReportType.ABSENTEE:
        table = "reporting_subscriber_ballotrequestreport"
        fields = ABSENTEE_FIELDS
    elif report.type == enums.ReportType.REGISTER:
        table = "reporting_subscriber_registerreport"
        fields = REGISTER_FIELDS
    elif report.type == enums.ReportType.VERIFY:
        table = "reporting_subscriber_verifyreport"
        fields = VERIFIER_FIELDS
    elif report.type == enums.ReportType.LOCATOR:
        table = "reporting_subscriber_locatorreport"
        fields = LOCATOR_FIELDS
    else:
        raise Exception("Invalid Report Type")

    if report.subscriber:
        sql = f"SELECT * FROM {table} WHERE subscriber_id = %s"
        args = [report.subscriber.uuid]
    else:
        sql = f"SELECT * FROM {table}"
        args = []

    new_file = StringIO()
    reportwriter = csv.writer(new_file)
    reportwriter.writerow([field[1] for field in fields])

    with connection.cursor() as cursor:
        cursor.execute(sql, args)
        columns = [col[0] for col in cursor.description]

        for row in cursor:
            row_dict = dict(zip(columns, row))

            new_row = []
            for field in fields:
                new_row.append(row_dict[field[0]])

            reportwriter.writerow(new_row)

    encoded_file_content = new_file.getvalue().encode("utf-8")

    item = StorageItem(
        app=enums.FileType.REPORT,
        email=report.author.email,
        subscriber=report.subscriber,
    )
    item.file.save(
        generate_name(report), ContentFile(encoded_file_content), True,
    )
    report.result_item = item
    report.status = enums.ReportStatus.COMPLETE
    report.save(update_fields=["result_item", "status"])
