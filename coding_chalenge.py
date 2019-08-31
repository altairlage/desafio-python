
import argparse
import boto3
import json
import datetime
from boto3.dynamodb.conditions import Key, Attr
from prettytable import PrettyTable


parser = argparse.ArgumentParser()

parser.add_argument(
    "--billing-file", "-b",
    action="store",
    required=True,
    help="The name of the billing file"
)


def main():
    args = parser.parse_args()
    billing_file = args.billing_file

    auth = boto3.Session(profile_name='wg-sandbox')
    ddb_resource = auth.resource('dynamodb')

    tb_customer = ddb_resource.Table('acampos-customer')
    tb_pricing = ddb_resource.Table('acampos-pricing')

    table = PrettyTable()
    table.field_names = ["Caller", "Target", "Start Time", "Duration", "Price"]

    call_list = read_billing_from_file(billing_file)
    final_price = 0

    for call in call_list:
        print('*** Call Info:')
        print(call)

        response = tb_customer.query(
            IndexName='customerNumber-index',
            KeyConditionExpression=Key('customerNumber').eq(call['callerNumber'])
        )

        # using the client:
        # response = ddb_client.query(
        #    TableName='acampos-customer',
        #    IndexName='customerNumber-index',
        #    ExpressionAttributeValues={
        #        ':v1': {
        #            'S': call['callerNumber'],
        #        },
        #    },
        #    KeyConditionExpression='customerNumber = :v1',
        # )

        # Get caller info:
        caller_data = response.get('Items')
        print('*** Caller data from DynamoDB table:')
        print(caller_data)

        # Get Target info:
        response = tb_customer.query(
            IndexName='customerNumber-index',
            KeyConditionExpression=Key('customerNumber').eq(call['targetNumber'])
        )
        target_data = response.get('Items')
        print('*** Target data from DynamoDB table:')
        print(target_data)

        # Get pricing info for the given user:
        response = tb_pricing.query(
            KeyConditionExpression=Key('offerId').eq(caller_data[0]['offerId'])
        )
        pricing_data = response.get('Items')
        print('*** Pricing data from DynamoDB table:')
        print(pricing_data)

        price = pricing_data[0]['price']
        call_price = price * call['duration']/60000 # price based in minutes
        final_price += call_price

        table.add_row([caller_data[0]['customerName'], target_data[0]['customerName'], get_pretty_full_date(call['startedTime']), get_pretty_duration(call['startedTime'], call['duration']), "R$ {}".format(call_price)])

    print('\n\n\n')
    print("Total price for the billing period is: R$ {}".format(final_price))
    print('Please find the details below:')
    print(table.get_string())


def get_pretty_full_date(date_in_millis):
    return datetime.datetime.fromtimestamp(date_in_millis/1000.0).strftime('%c')


def get_pretty_duration(start_date_in_millis, duration_in_millis):
    start = datetime.datetime.fromtimestamp(start_date_in_millis / 1000.0)
    endmillis = start_date_in_millis + duration_in_millis
    end = datetime.datetime.fromtimestamp(endmillis / 1000.0)
    delta = end - start
    return str(delta)

def read_billing_from_file(billing_file):
    with open(billing_file, 'r') as f:
        billing_dict = json.load(f)

    return billing_dict


if __name__ == '__main__':
    main()

