import json, logging, math, pandas, re
from datetime import datetime, timedelta

NIGHTLY_FEE = 0.36
PERMANENT_FEE = 0.36
MINUTE_FEE = 0.09
DAY_HOUR = 6
NIGHT_HOUR = 22

logging.basicConfig(level=logging.DEBUG)

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]

def is_valid(record) -> bool:
    if record is None:
        raise Exception('Null object')

    if record['source'] is None:
        raise Exception('Source field is missing')

    if record['destination'] is None:
        raise Exception('Destination field is missing')

    if record['start'] is None:
        raise Exception('Start field is missing')

    if record['end'] is None:
        raise Exception('End field is missing')

    if type(record['start']) is not int:
        raise Exception('Start is not a integer')

    if type(record['end']) is not int:
        raise Exception('End is not a integer')

    # Windows validation 01/01/1970
    if record['start'] < 86400:
        raise Exception('Start epoch {} is out of range'.format(record['start']))

    if record['end'] < 86400:
        raise Exception('End epoch {} is out of range'.format(record['end']))

    # Only 99-999999999 format
    rgxpattern = '^[0-9]{2}-[0-9]{9}$'
    regexp = re.compile(rgxpattern)

    if not regexp.match(record['source']):
        raise Exception('Source {} is not a valid phone number'.format(record['source']))

    if not regexp.match(record['destination']):
        raise Exception('Destination {} is not a valid phone number'.format(record['destination']))

    return True


def get_day_cycles(dt_start, dt_end):
    """
        Day cycles are charged in minutes
    """
    qtt = 0

    if dt_start < dt_end and (DAY_HOUR <= dt_start.hour < NIGHT_HOUR):
        dt_new_start = dt_start + timedelta(hours=24)
        # just in case duration extends more than one day
        qtt = (dt_end - dt_start).seconds/60 + get_day_cycles(dt_new_start, dt_end)
    return qtt

def get_night_cycles(dt_start, dt_end) -> int:
    """
        Night cycles are charged in days
    """
    qtt = 0

    if dt_start < dt_end and (dt_start.hour < DAY_HOUR or dt_start.hour >= NIGHT_HOUR):
        dt_new_start = dt_start + timedelta(hours=24)
        # just in case duration extends more than one day
        qtt = 1 + get_night_cycles(dt_new_start, dt_end)
    return qtt

def calculate_fee(start, end):
    dt_start = datetime.fromtimestamp(start)
    dt_end = datetime.fromtimestamp(end)

    logging.debug('Start {} End {}'.format(
        dt_start.strftime('%d/%m/%Y, %H:%M:%S'),
        dt_end.strftime('%d/%m/%Y, %H:%M:%S')))

    # DAY: have to be complete cycle
    day_cycles = math.trunc(get_day_cycles(dt_start, dt_end))

    logging.debug('Day cycles {}'.format(day_cycles))

    day_fee = 0
    if day_cycles > 0:
        day_fee = round(PERMANENT_FEE + (day_cycles * MINUTE_FEE), 2)
    
    logging.debug('Day fee {}'.format(day_fee))

    # NIGHT
    night_cycles = get_night_cycles(dt_start, dt_end)

    logging.debug('Night cycles {}'.format(night_cycles))
    
    night_fee = round(NIGHTLY_FEE * night_cycles, 2)

    logging.debug('Night fee {}'.format(night_fee))

    return day_fee + night_fee

def classify_by_phone_number(records):
    result = []

    for record in records:
        try:
            if is_valid(record):

                logging.debug('Phone {}'.format(record['source']))

                record['fee'] = calculate_fee(record['start'], record['end'])

                logging.debug('Total Fee {}'.format(record['fee']))

                result.append({ 'source': record['source'], 'total': record['fee']})

        except Exception as ex:
            logging.error(ex)
    
    # aggregate data
    df_result = pandas.DataFrame(result).groupby('source').sum().reset_index()

    s_json_result =  df_result.sort_values('total', ascending=False).to_json(orient='records')
    return json.loads(s_json_result)
