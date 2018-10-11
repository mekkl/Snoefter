from scapy.all import sniff
from scapy.packet import Packet
import logging


######## Main ########

def main():
    http_sniff_logger()
    #http_sniffer()



######## Top level functions ########

def http_sniffer(method='GET', filter='tcp port 80', count=0):
    '''Top level function

    '''

    raw = []
    sniff(count=count, filter=filter, prn=lambda x: raw.append(x))

    http_data = _http_packets_aslist(raw, method)

    print(http_data)


def http_sniff_logger(method='GET', filter='tcp port 80', count=0):
    '''Top level function

    '''

    logging.basicConfig(filename=f'http.{method}.log', level=logging.INFO)

    sniff(count=count, filter=filter, prn=lambda x: _http_packets_logger(x, method))



######## Filter functions ########

def _http_parser(packet, method='GET'):
    ''' Parsing packet to a python dictionary

    '''

    packet_str = str(packet)
    index_get = packet_str.find(method)
    req = {}

    # IP information of source and destination
    req['IP_src'] = packet.getlayer('IP').src
    req['IP_dst'] = packet.getlayer('IP').dst

    parsing = ''.join(packet_str[index_get:]) # only get part containing http data
    headers_list = parsing.split('\\r\\n') # split between different headers

    req['Method'] = headers_list[0][0:4] # first item is always the method

    # run through rest of request data and pull out header data
    for i in range(1, len(headers_list)):
        h_type = headers_list[i][0: headers_list[i].find(':')] # get header type
        req[h_type] = headers_list[i][headers_list[i].find(':') + 2:] # set header type/value
        
    return req


######## Logger functions ########

def _http_packets_logger(packet, method='GET'):

    if str(packet).find(method) > 0:
        logging.log(logging.INFO, _http_parser(packet, method))



######## To python-collection functions ########

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


######## div ########

def tostring(packet):
    return(str(packet))


if __name__ == '__main__':
    main()