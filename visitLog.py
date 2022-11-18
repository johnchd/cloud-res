import boto3
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

counter_table = boto3.resource('dynamodb').Table('visitLogDB')

def lambda_handler(event, context):
    response = counter_table.update_item(
        Key={'siteviews': 'view_counter'},
        ExpressionAttributeValues={':inc': decimal.Decimal(1)},
        UpdateExpression="ADD counter_value :inc"
    )
    
    item = counter_table.get_item(Key={'siteviews': 'view_counter'})
    count_views = item['Item']['counter_value']
    return(count_views)
