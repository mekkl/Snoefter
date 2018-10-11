from scapy.all import sniff
import logging

def _http_sniffer(method='GET', filter='tcp port 8081', count=30):
    raw = []
    sniff(count=count, filter=filter, prn=lambda x: raw.append(x))

    http_data = _http_packets_aslist(raw, method)

    print(http_data)


def http_sniff_logger(method='GET', filter='tcp port 8081', count=30):
    logging.basicConfig(filename=f'http.{method}.log', level=logging.INFO)

    sniff(count=count, filter=filter, prn=lambda x: _http_packets_logger(x, method))


def _http_packets_logger(packet, method='GET'):

    if str(packet).find(method) > 0:
        logging.log(logging.INFO, _http_parser(packet, method))


def _http_parser(packet, method='GET'):
    packet_str = str(packet)
    index_get = packet_str.find(method)
    req = {}

    parsing = ''.join(packet_str[index_get:]) # only get part containing http data
    headers_list = parsing.split('\\r\\n') # split between different headers
    
    req['Method'] = headers_list[0] # first item is always the method

    # run through rest of request data and pull out header data
    for i in range(1, len(headers_list)):
        h_type = headers_list[i][0: headers_list[i].find(':')] # get header type
        req[h_type] = headers_list[i][headers_list[i].find(':') + 2:] # set header type/value
        
    return req


def _http_packets_aslist(raw_packets, method='GET'):
    ''' Returns a list of dictionaries, containing request data
        Params:
            list(str): raw_packets
            str: method
        Returns:
            list(dictionaries): packets 
    '''

    packets = [_http_parser(packet, method) for packet in raw_packets if str(packet).find(method) > 0]
    return packets
        
        
def http_packets_generator(raw_packets, method='GET'):
    ''' Returns a generator of dictionaries, containing request data
        Params:
            list(str): raw_packets
            str: method
        Returns:
            generator(dictionaries): packets 
    '''

    packets = (_http_parser(packet) for packet in raw_packets if str(packet).find(method) > 0)
    return packets

def tostring(packet):
    return(str(packet))


if __name__ == '__main__':
    http_sniff_logger()