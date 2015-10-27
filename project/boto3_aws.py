__author__ = 'atsvetkov'


from boto3.session import Session
from prettytable import PrettyTable
import datetime
import argparse
from pprint import pprint as pp


def get_tango_aws_dict(default_region="us-east-1", arg_instance_state=None):

    session = Session(aws_access_key_id='',
                      aws_secret_access_key='',
                      region_name=default_region
                      )

    # ec2 client session (default region):
    ec2_client = session.client('ec2')

    # get all regions:
    regions = ec2_client.describe_regions()
    regions_names = list(map(lambda _: _['RegionName'], regions['Regions']))

    # create tango_aws_dict:
    # {<aws_region>: <list of dicts with instance info>}
    tango_aws_dict = {}
    for region in regions_names:
        ec2_instances_objs = session.resource('ec2', region_name=region).instances.all()

        ec2_instances_list = []
        for ec2_instance_obj in ec2_instances_objs:
            # create dict per each instance:
            ec2_instance_dict = {
                "instance_id": ec2_instance_obj.instance_id,
                "instance_type": ec2_instance_obj.instance_type,
                # "tags": ec2_instance_obj.tags,
                "tags": tag_parser(ec2_instance_obj.tags),
                "image_id": ec2_instance_obj.image_id,
                "state": ec2_instance_obj.state['Name'],
                "public_dns_name": ec2_instance_obj.public_dns_name,
                "private_dns_name": ec2_instance_obj.private_dns_name,
                "public_ip_address": ec2_instance_obj.public_ip_address,
                "private_ip_address": ec2_instance_obj.private_ip_address
            }

            # create list of ec2_info dicts per region:
            # filter "ec2_instance_dict" by instance_state:
            if arg_instance_state == "all":
                ec2_instances_list.append(ec2_instance_dict.copy())
            elif ec2_instance_dict['state'] == arg_instance_state:
                ec2_instances_list.append(ec2_instance_dict.copy())
            else:
                continue

        try:
            # try to sort this list by multiple fields:
            ec2_instances_list_sorted = sorted(ec2_instances_list.copy(), key=lambda _: (_["tags"]["Name"],
                                                                                         _["tags"]["aws:autoscaling:groupName"],
                                                                                         _["instance_type"]))
        except TypeError:
            pass

        tango_aws_dict[region] = ec2_instances_list_sorted



    # DEBUG:
    # pp(tango_aws_dict)

    return tango_aws_dict


def tag_parser(ec2_instance_obj_tags):

    # DEBUG:
    # pp(ec2_instance_obj_tags)

    # define set of required tags:
    ec_2_instance_tags_dict = {"Name": "-",
                               "service": "-",
                               "application": "-",
                               "group": "-",
                               "role": "-",
                               "aws:autoscaling:groupName": "-"}

    # get all required tags:
    for tag_name in ec_2_instance_tags_dict:
        try:
            for tag_kv_dict in ec2_instance_obj_tags:
                if tag_name == tag_kv_dict["Key"]:
                    ec_2_instance_tags_dict[tag_name] = tag_kv_dict["Value"]
        except TypeError:
            continue

    # DEBUG:
    # pp(ec_2_instance_tags_dict)

    return ec_2_instance_tags_dict.copy()


def tango_aws_dict_pretty_print(tango_aws_dict, arg_aws_region=None, arg_report_type=None):

    # Define all possible AWS regions:
    aws_regions_all = {
        "us-east-1": ["US East (N. Virginia)", "us06"],
        "us-west-2": ["US West (Oregon)", "us07"],
        "us-west-1": ["US West (N. California)", "-"],
        "eu-west-1": ["EU (Ireland)", "ie01"],
        "eu-central-1": ["EU (Frankfurt)", "de01"],
        "ap-southeast-1": ["Asia Pacific (Singapore)", "sg01"],
        "ap-southeast-2": ["Asia Pacific (Sydney)", "au01"],
        "ap-northeast-1": ["Asia Pacific (Tokyo)", "jp01"],
        "sa-east-1": ["South America (Sao Paulo)", "br01"]}

    # DEBUG:
    # pp(tango_aws_dict)

    # create list of tuples (<region>, <number of instances>), sorted by number of instances in region:
    tango_aws_list_summary = sorted([(k, len(v)) for k, v in tango_aws_dict.items()], key=lambda _: _[1], reverse=True)
    # DEBUG:
    # pp(tango_aws_list_summary)

    # PRETTY TABLES (summary and detailed):

    # list names of columns in summary table:
    summary_table = PrettyTable(["Region", "Location", "Site", "Count"])
    summary_table.align = "l"  # Left align.
    summary_table.padding_width = 1  # One space between column edges and contents (default)

    # dict for storing detailed tables: {"<region>": "<pretty_table_obj>"}
    details_tables_dict = {}

    for summary_row in tango_aws_list_summary:
        ec2_region, ec2_count = summary_row
        ec2_location, ec2_site = aws_regions_all[ec2_region]

        # create summary table:
        summary_table.add_row([ec2_region, ec2_location, ec2_site, ec2_count])

        # create details table per region:
        # list names of columns for details table:
        details_table = PrettyTable([
            "ID",
            "Tag Name",
            "Tag Service",
            "Tag Application",
            # "Tag group",
            # "Tag Role",
            "Tag ASG",
            "Type",
            # "Image ID",
            "State",
            # "Public DNS Name",
            # "Private DNS Name",
            "Private IP Address",
            # "Public IP Address"
        ])

        details_table.align = "l"
        details_table.padding_width = 1

        for ec2_info_dict in tango_aws_dict[ec2_region]:
            details_table.add_row([
                ec2_info_dict["instance_id"],
                ec2_info_dict["tags"]["Name"],
                ec2_info_dict["tags"]["service"],
                ec2_info_dict["tags"]["application"],
                # ec2_info_dict["tags"]["group"],
                # ec2_info_dict["tags"]["role"],
                ec2_info_dict["tags"]["aws:autoscaling:groupName"],
                ec2_info_dict["instance_type"],
                # ec2_info_dict["image_id"],
                ec2_info_dict["state"],
                # ec2_info_dict["public_dns_name"],
                # ec2_info_dict["private_dns_name"],
                ec2_info_dict["private_ip_address"],
                # ec2_info_dict["public_ip_address"]
            ])

        details_tables_dict[ec2_region] = details_table

    # DEBUG:
    # print("REPORT TIME:", datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y"))
    # print("SUMMARY INFORMATION:")
    # print(summary_table)
    # print()
    # print("DETAILED INFORMATION:")
    # for region, details_table in details_tables_dict.items():
    #     print()
    #     print(region)
    #     print(details_table)

    def print_summary():
        print("SUMMARY INFORMATION:")
        print(summary_table)

    def print_details():
        print("DETAILED INFORMATION:")
        # regions in sort order:
        for region in [data_tuple[0] for data_tuple in tango_aws_list_summary]:
            print()
            print(region)
            print(details_tables_dict[region])

    # PRINT REPORT:
    print("REPORT TIME:", datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y")+"\n")
    if arg_aws_region != 'all' and arg_report_type != 'summary':
        print(details_tables_dict[[k for k, v in aws_regions_all.items() if v[1] == arg_aws_region][0]])
    elif arg_report_type == 'summary':
        print_summary()
    elif arg_report_type == 'details':
        print_details()
    elif arg_report_type == 'full':
        print_summary()
        print_details()

    # pp(dir(summary_table))
    # print(summary_table.get_html_string())

    return summary_table, details_tables_dict


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--instance_state", help="choose state of instance", default='running', choices=['running',
                                                                                                         'stopped',
                                                                                                         'all'])
    parser.add_argument("--aws_region", help="choose AWS region", default='all', choices=['us06',
                                                                                          'us07',
                                                                                          'ie01',
                                                                                          'de01',
                                                                                          'sg01',
                                                                                          'au01',
                                                                                          'jp01',
                                                                                          'br01',
                                                                                          'all'])
    parser.add_argument("--report_type", help="choose report type", default='full', choices=['summary',
                                                                                             'details',
                                                                                             'full'])
    args = parser.parse_args()
    # DEBUG:
    # print(args)

    tango_aws_dict_pretty_print(get_tango_aws_dict(arg_instance_state=args.instance_state),
                                arg_aws_region=args.aws_region,
                                arg_report_type=args.report_type)

if __name__ == '__main__':
    main()

