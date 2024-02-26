import argparse
import re
import hashlib
import binascii

try:
    from Crypto.Cipher import AES
    from Crypto.Util import Counter
except ImportError:
    print('"pycryptodome" module is required for uuid generation')
    exit()


class OpaqueId:
    """
    An arbitrary 12-byte string to pad our 4-byte IV up to the required 16 bytes
    """
    IV_PADDER = 'the_magic_12'

    DEBUG = False

    null_result = {
        'id': None,
        'country': None,
    }

    @staticmethod
    def get_params_by_id_and_country(id, iso):
        """
        Returns parameters for encryption

        :param int id:
        :param str iso:

        :return dict:
        """
        country_hash = hashlib.sha1(iso.encode()).hexdigest()

        iv = hashlib.sha1((country_hash + str(id)).encode()).hexdigest()

        return {
            'country': iso,
            'visible_1': country_hash[0:4],
            'visible_2': country_hash[4:8],
            'password': country_hash[-8:],
            'iv': iv[8:12],
        }

    @staticmethod
    def to_8_byte_string(data):
        """
        Transform an integer into an 8-byte string based on its binary value

        :param int data: The integer to transform

        :return str: The resulting 8-byte string
        """
        transformed = ''

        for i in range(8):
            shift = (7 - i) * 8
            code = (data & (0xff << shift)) >> shift & 0xFF
            transformed += chr(code)

        transformed = transformed.encode('iso-8859-1')
        print('8_byte_string:', binascii.hexlify(transformed)) if OpaqueId.DEBUG else None

        return transformed

    @staticmethod
    def from_8_byte_string(data):
        """
        Transform an 8-byte string to an integer

        :param bytes data: The string to transform

        :return int: The resulting integer
        """
        data = data.decode('iso-8859-1')
        transformed = 0

        for i in range(8):
            char = data[i]
            val = ord(char)
            shift = (7 - i) * 8
            transformed |= (val << shift)

        return transformed

    @staticmethod
    def int_of_string(s):
        return int(binascii.hexlify(s), 16)

    @staticmethod
    def get_cipher(country_params):
        iv = OpaqueId.IV_PADDER + country_params['iv']

        counter = Counter.new(128, initial_value=OpaqueId.int_of_string(iv.encode()))

        key = country_params['password'].ljust(32, "\0").encode()

        cipher = AES.new(key, AES.MODE_CTR, counter=counter)

        return cipher

    @staticmethod
    def encrypt_id(id, country_params):
        """
        Encrypt the original ID using country info to manage the encryption

        :param int id: The ID to encrypt
        :param dict country_params: dict containing the country info

        :return str: The encrypted ID
        """
        cipher = OpaqueId.get_cipher(country_params)
        result = cipher.encrypt(OpaqueId.to_8_byte_string(id))

        return binascii.hexlify(result).decode()

    @staticmethod
    def decrypt_id(encrypted_id, country_params):
        """
        Decrypt the ID using country info to manage the decryption

        :param str encrypted_id: The ID to decrypt
        :param dict country_params: dict containing the country info

        :return int: The decrypted ID
        """
        cipher = OpaqueId.get_cipher(country_params)
        decrypted_id = cipher.decrypt(binascii.unhexlify(encrypted_id))
        print('decrypted_id', decrypted_id) if OpaqueId.DEBUG else None

        return OpaqueId.from_8_byte_string(decrypted_id)

    @staticmethod
    def encode_partial_uuid(encrypted_id, country_params):
        """
        Encode the partial Uuid in the right format based on ID/Country parameters

        :param str encrypted_id:
        :param dict country_params:

        :return str:
        """
        id_pieces = {
            'hi': encrypted_id[0:4],
            'mid_hi': encrypted_id[4:8],
            'mid_lo': encrypted_id[8:12],
            'lo': encrypted_id[12:16],
        }

        partial_uuid = '{}-{}-{}-{}-{}{}{}'.format(
            country_params['iv'],
            id_pieces['hi'],
            country_params['visible_1'],
            id_pieces['lo'],
            country_params['visible_2'],
            id_pieces['mid_hi'],
            id_pieces['mid_lo']
        )

        return partial_uuid

    @staticmethod
    def decode_partial_uuid(partial_uuid):
        """
        Decode the partial Uuid based on ID/Country parameters

        :param str partial_uuid: The UUID to decode

        :return dict:
        """
        country_params = {
            'visible_1': partial_uuid[10:14],
            'visible_2': partial_uuid[20:24],
            'iv': partial_uuid[0:4],
        }

        country_short_hash = country_params['visible_1'] + country_params['visible_2']
        iso = OpaqueId.get_country_by_hash(country_short_hash)

        country_hash = hashlib.sha1(
            iso.encode() if iso is not None else b''
        ).hexdigest()

        country_params['password'] = country_hash[-8:]
        country_params['country'] = iso

        id_pieces = {
            'hi': partial_uuid[5:9],
            'mid_hi': partial_uuid[24:28],
            'mid_lo': partial_uuid[28:32],
            'lo': partial_uuid[15:19]
        }

        return {
            'encrypted_id': id_pieces['hi'] + id_pieces['mid_hi'] + id_pieces['mid_lo'] + id_pieces['lo'],
            'country_params': country_params
        }

    @staticmethod
    def compute_signature(partial_uuid):
        """Compute the signature of a partial UUID

        :param string partial_uuid: The UUID to sign
        :return: string
        """
        return hashlib.sha1(partial_uuid.encode()).hexdigest()[0:4]

    @staticmethod
    def generate_uuid(id, iso='fr'):
        """
        Generate a UUID-like ID, based on the country and the original ID.

        :param int id: The original ID of a resource
        :param str iso: The country for which the id is used

        :return str:
        """
        country_params = OpaqueId.get_params_by_id_and_country(id, iso)
        print('country_params', country_params) if OpaqueId.DEBUG else None

        encrypted_id = OpaqueId.encrypt_id(id, country_params)
        print('encrypted_id', encrypted_id) if OpaqueId.DEBUG else None

        partial_uuid = OpaqueId.encode_partial_uuid(encrypted_id, country_params)
        print('partial_uuid', partial_uuid) if OpaqueId.DEBUG else None

        signature = OpaqueId.compute_signature(partial_uuid)
        print('signature', signature) if OpaqueId.DEBUG else None

        return '{}{}'.format(signature, partial_uuid)

    @staticmethod
    def get_country_by_hash(short_hash):
        """
        Return country's ISO code by short hash

        :param str short_hash: Hash of the country

        :return str|None:
        """
        lookup = {
            '4aeb195c': 'ad',
            '1eabdaf4': 'ae',
            'd1e62250': 'af',
            '7edd1dd2': 'ag',
            '141a9241': 'ai',
            '2f9ee2b3': 'al',
            '96e81557': 'am',
            'c29dd6c8': 'ao',
            'b3a7c645': 'aq',
            '23d8e015': 'ar',
            'df211ccd': 'as',
            '27e90dfa': 'at',
            'f095160c': 'au',
            'a7ce5b0c': 'aw',
            '2a2e1206': 'ax',
            '90283840': 'az',
            '6c0596b8': 'ba',
            '9a900f53': 'bb',
            'e3f284ca': 'bd',
            '986b1bc1': 'be',
            'dba89299': 'bf',
            '80f87c88': 'bg',
            '6de8967f': 'bh',
            'aab9b7bd': 'bi',
            '3d26bb39': 'bj',
            'f55fb781': 'bl',
            'a67acd6e': 'bm',
            '19f38987': 'bn',
            'dc45fe02': 'bo',
            '85250a8f': 'bq',
            '3eb65786': 'br',
            'f33330b1': 'bs',
            'edfb92a5': 'bt',
            '1fd5892d': 'bv',
            '8a85c06c': 'bw',
            '40815864': 'by',
            '0c17ddce': 'bz',
            '1c42c72c': 'ca',
            'bdb480de': 'cc',
            '03477819': 'cd',
            'f78b64c9': 'cf',
            'bb0b6647': 'cg',
            '482bd64c': 'ch',
            '5a4fe083': 'ci',
            'c8c2ca9f': 'ck',
            'ef3ecccf': 'cl',
            'e283e1df': 'cm',
            'b0bc9abd': 'cn',
            '87dda204': 'co',
            'ccd8c159': 'cr',
            '164c4a27': 'cv',
            '8e425ff7': 'cw',
            '6eeb3fec': 'cx',
            '31ace4ad': 'cy',
            '763e59c2': 'cz',
            '600ccd1b': 'de',
            '10099878': 'dj',
            'd5658db4': 'dk',
            '8f489e76': 'dm',
            'eadcd9bd': 'do',
            '57f378cc': 'dz',
            '7dd84750': 'ec',
            '1f444844': 'ee',
            '3a1c21a5': 'eg',
            '706a483d': 'eh',
            '602c57ff': 'er',
            '09cd68a2': 'es',
            'a5bc1d9b': 'et',
            '6b163fa3': 'fi',
            '0beff6db': 'fj',
            'cacdf082': 'fk',
            'adeb6f2a': 'fm',
            '19082866': 'fo',
            'b858a87c': 'fr',
            '72b6ef47': 'ga',
            '61fc7bcf': 'gb',
            '43d3eca4': 'gd',
            'a9060bd5': 'ge',
            '4ebb4595': 'gf',
            'f3226f91': 'gg',
            '1041179c': 'gh',
            'fc7794c8': 'gi',
            '5644a3f6': 'gl',
            'd2d359e4': 'gm',
            'd4f83415': 'gn',
            '4af17906': 'gp',
            '4cbc5070': 'gq',
            'de061098': 'gr',
            '3b15a4ea': 'gs',
            '7ddf988c': 'gt',
            '81dbcb91': 'gu',
            'fc471ce1': 'gw',
            '1fd642f1': 'gy',
            '4fe0d242': 'hk',
            '4ffa4b4f': 'hm',
            '59889052': 'hn',
            '51bd9535': 'hr',
            '80f6b1db': 'ht',
            '06b08b32': 'hu',
            '87ea5dfc': 'id',
            '46680a66': 'ie',
            '53c1d6af': 'il',
            '42a0d306': 'im',
            'af10ef20': 'in',
            '5a258230': 'io',
            'a07d6616': 'iq',
            'b47f363e': 'is',
            '6c5522ca': 'it',
            '68d2ad23': 'je',
            '112f489f': 'jm',
            'bd73d357': 'jo',
            '0f41a0b3': 'jp',
            '15d5e1d3': 'ke',
            '1389845b': 'kg',
            'e26bcf26': 'kh',
            '81d21110': 'ki',
            '08ec69f5': 'km',
            '5c0795f5': 'kn',
            '513c04e7': 'kp',
            'faf8d203': 'kr',
            '5f1c0be8': 'kw',
            '21ab7080': 'ky',
            'efb215f8': 'kz',
            '3efd4c0f': 'la',
            'cba41814': 'lb',
            '7a01ac07': 'lc',
            '41db30f8': 'li',
            '9b20e9ff': 'lk',
            '1370e957': 'lr',
            'ebfdec64': 'ls',
            '5f3acfbe': 'lt',
            '3f76228c': 'lu',
            '4d73c29a': 'lv',
            'ec594490': 'ly',
            '1382244e': 'ma',
            'dcab2065': 'mc',
            '240c4df7': 'md',
            'b1c1d873': 'me',
            '5d838ec8': 'mf',
            '191be371': 'mg',
            '99044191': 'mh',
            'a91dcbb4': 'mk',
            'b331fc67': 'ml',
            'b8d09b4d': 'mm',
            '78dc0cd3': 'mn',
            '6adbae8c': 'mo',
            '91f6e575': 'mp',
            'efe3c558': 'mq',
            '8e7be411': 'mr',
            '26cc3217': 'ms',
            '0658929a': 'mt',
            '1247e024': 'mu',
            '362d60cb': 'mv',
            '99c15d92': 'mw',
            '3ab846d5': 'mx',
            '3ece1471': 'my',
            'e688cf74': 'mz',
            '5efb4ac2': 'na',
            'e0422724': 'nc',
            'f60d2a2f': 'ne',
            '0cdd8b5e': 'nf',
            '7d65c4e2': 'ng',
            'c5f2aaa8': 'ni',
            '595477bd': 'nl',
            'fd128635': 'no',
            '003fffd5': 'np',
            'a8643e0e': 'nr',
            '539e0278': 'nu',
            '5cea5a51': 'nz',
            '83db8932': 'om',
            '379fc0d5': 'pa',
            '1db828bc': 'pe',
            '586de3e9': 'pf',
            '96dd8d96': 'pg',
            '8df74dda': 'ph',
            '6924110c': 'pk',
            'f437cb07': 'pl',
            'c4dcbb4b': 'pm',
            '51d55774': 'pn',
            '5498d9b9': 'pr',
            'c67f1ee1': 'ps',
            'bc811258': 'pt',
            '1a91d62f': 'pw',
            '902afd88': 'py',
            'd3c58341': 'qa',
            'c387c982': 're',
            'eed1903a': 'ro',
            '03aae0c3': 'rs',
            '67b8b1c4': 'ru',
            '35d495b4': 'rw',
            '3608a6d1': 'sa',
            'b70482a9': 'sb',
            '04096ad9': 'sc',
            '4452d716': 'sd',
            '00762ccf': 'se',
            'ff397964': 'sg',
            '16795633': 'sh',
            '7dd9b338': 'si',
            '56c5295c': 'sj',
            '766a6e89': 'sk',
            '2b002dcf': 'sl',
            '3e76c243': 'sm',
            'c3ecef83': 'sn',
            'cd1b646e': 'so',
            '44b7497c': 'sr',
            'c1c93f88': 'ss',
            '9b02d997': 'st',
            '0a6190df': 'sv',
            'c7fff82d': 'sx',
            '1d4daae7': 'sy',
            'c57c8e6d': 'sz',
            'd61e3363': 'tc',
            'c156a3b8': 'td',
            'e6c9da68': 'tf',
            'e4b203cd': 'tg',
            'fa6af6e9': 'th',
            '546b0590': 'tj',
            '4f8f608a': 'tk',
            '5e2cbfa6': 'tl',
            'a547db31': 'tm',
            'b295c12c': 'tn',
            '4374aaee': 'to',
            'd9e83874': 'tr',
            '8c101798': 'tt',
            'ff0dc9ba': 'tv',
            '9cd92c51': 'tw',
            '1412349a': 'tz',
            '1589fe07': 'ua',
            '8b438931': 'ug',
            '68c42a32': 'uk',
            'ec92b743': 'um',
            'da2b1288': 'us',
            '2b2dfac4': 'uy',
            'f1950b3f': 'uz',
            '665a4dc9': 'va',
            '7d956a61': 'vc',
            '934cff2d': 've',
            '6f398128': 'vg',
            '833da188': 'vi',
            '3285442f': 'vn',
            'a29d050b': 'vu',
            '78991a54': 'wf',
            '1457b75d': 'ws',
            'f9473937': 'ye',
            '4932b0da': 'yt',
            '85c9baff': 'za',
            '161c0aad': 'zm',
            'e1f2c92f': 'zw',
        }

        return lookup[short_hash] if short_hash in lookup else None

    @staticmethod
    def decode_uuid(uuid):
        """
        Retrieve the original ID/Country pair used to generate a given UUID

        :param str uuid: The UUID to decode

        :return dict:
        """
        if not re.match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', uuid):
            return OpaqueId.null_result

        signature = uuid[0:4]
        partial_uuid = uuid[4:]

        if OpaqueId.compute_signature(partial_uuid) != signature:
            return OpaqueId.null_result

        data = OpaqueId.decode_partial_uuid(partial_uuid)
        print('data', data) if OpaqueId.DEBUG else None

        if data['country_params']['country'] is None:
            return OpaqueId.null_result

        decrypted_id = OpaqueId.decrypt_id(data['encrypted_id'], data['country_params'])

        return {
            'id': decrypted_id,
            'country': data['country_params']['country']
        }

    @staticmethod
    def uuid_to_id(uuid):
        """
        Retrieve the original ID from a given UUID

        :param str uuid: The UUID to decode

        :return int: The original ID
        """
        result = OpaqueId.decode_uuid(uuid)
        print('result', result) if OpaqueId.DEBUG else None

        return result['id']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encode id to uuid as well as decode id from uuid')
    parser.add_argument('input', help='[id] to encode or [uuid] to decode')
    parser.add_argument('iso', help='country code which will be used for encode/decode', default='fr', nargs='?')
    args = parser.parse_args()

    if re.match('^[0-9]+$', args.input):
        print(OpaqueId.generate_uuid(int(args.input), args.iso))
    else:
        print(OpaqueId.uuid_to_id(args.input))
