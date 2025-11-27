"""
Script to add all Manipur Police Stations to the database
"""
from extensions import mongo
from datetime import datetime
from config import Config

# Initialize Flask app context
from flask import Flask
app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

# Police Stations Data
stations_data = [
    {"name": "Imphal Police Station", "code": "IPS", "area": "Imphal", "address": "Sanakhwa Yaima Kollup, Imphal, Manipur 795001", "district": "Imphal West"},
    {"name": "Manipur Police Headquarter", "code": "PHQ", "area": "Imphal", "address": "Indo-Myanmar Road, NH-39, Sanakhwa Yaima Kollup, Babupara, Imphal, Manipur 795001", "district": "Imphal West"},
    {"name": "City Police Station", "code": "CPS", "area": "Imphal", "address": "Gandhi Avenue, Thangal Bazar, Imphal, Manipur 795001", "district": "Imphal West"},
    {"name": "Singjamei Police Station", "code": "SJPS", "area": "Imphal", "address": "Indo-Myanmar Rd, Lairembi Lampak, Waikhom Leikai, Imphal, Manipur 795003", "district": "Imphal West"},
    {"name": "Kwakeithel Police Station", "code": "KWPS", "area": "Imphal", "address": "Lourembam Leikai, Imphal, Manipur 795001", "district": "Imphal West"},
    {"name": "Porompat Police Station", "code": "PPS", "area": "Leikai", "address": "Thawanthaba Leirak, Imphal, Lairikyengbam Leikai, Manipur 795005", "district": "Imphal East"},
    {"name": "Lamphel Police Station", "code": "LPS", "area": "Lamphelpat", "address": "Lamphelpat, Imphal, Manipur 795004", "district": "Imphal West"},
    {"name": "Mayang Imphal Police Station", "code": "MIPS", "area": "Mayai Lambi Road", "address": "Mayai Lambi Rd, Mayang Imphal, Manipur 795132", "district": "Imphal West"},
    {"name": "Patsoi Police Station", "code": "PAPS", "area": "Lamshang", "address": "Lamshang, Manipur 795113", "district": "Imphal West"},
    {"name": "Irilbung Police Station", "code": "IRPS", "area": "Kalika", "address": "Irilbung Bridge Rd, Kalika, Manipur 795008", "district": "Imphal West"},
    {"name": "Wangoi Police Station", "code": "WPS", "area": "Wangoi", "address": "Wangoi, Manipur 795009", "district": "Imphal West"},
    {"name": "Lamlais Police Station", "code": "LLPS", "area": "Lamlais", "address": "National Highway 150, Manipur 795010", "district": "Imphal East"},
    {"name": "Bishnupur Police Station", "code": "BPS", "area": "Bishnupur", "address": "Bishnupur, Manipur 795126", "district": "Bishnupur"},
    {"name": "Heingang Police Station", "code": "HPS", "area": "Heingang", "address": "Heingang Rd, Imphal, Manipur 795002", "district": "Imphal East"},
    {"name": "Moirang Police Station", "code": "MPS", "area": "Moirang", "address": "Tipaimukh Rd, Pasang Leikai, Moirang, Manipur 795133", "district": "Bishnupur"},
    {"name": "Mainpur Police Station", "code": "MAPS", "area": "Maphou Dam Road", "address": "Maphou Dam Rd, Manipur 795145", "district": "Tengnoupal"},
    {"name": "Waikhong Police Station", "code": "WKPS", "area": "Waikhong", "address": "Waikhong, Manipur 795103", "district": "Thoubal"},
    {"name": "Keibul Police Station", "code": "KBPS", "area": "Bishnupur", "address": "Keibul Lamjao Rd, Bishnupur, Manipur 795133", "district": "Bishnupur"},
    {"name": "Loktak Police Station", "code": "LKPS", "area": "Loktak", "address": "Ningthoukhong, Zero Colony, Loktak, Manipur 795126", "district": "Bishnupur"},
    {"name": "Saikul Police Station", "code": "SKPS", "area": "Senapati", "address": "Saikul Road, Sadar Hills, Senapati, Manipur 795118", "district": "Kangpokpi"},
    {"name": "Andro Police Station", "code": "ANPS", "area": "Yairipok Road", "address": "Angtha - Yairipok Road, Top-Chingtha, Manipur 795149", "district": "Imphal East"},
    {"name": "Sangaikot Police Station", "code": "SGPS", "area": "Churachandpur", "address": "Churachandpur, Manipur 795101", "district": "Churachandpur"},
    {"name": "Moreh Police Station", "code": "MRPS", "area": "Moreh", "address": "Indo-Myanmar Rd, Moreh, Manipur", "district": "Tengnoupal"},
    {"name": "Reserved Police Station", "code": "RPS", "area": "Senapati", "address": "Mao Church Rd, Senapati, Manipur 795106", "district": "Senapati"},
    {"name": "Awang Sekmai Police Station", "code": "ASPS", "area": "Sekmai Bazar", "address": "Awang Sekmai, Sekmai Bazar, Manipur 795136", "district": "Imphal West"},
    {"name": "Yairipok Police Station", "code": "YAPS", "area": "Yairipok", "address": "Pechi Village Rd, Yairipok, Manipur 795149", "district": "Imphal East"},
    {"name": "Women Police Station", "code": "WMPS", "area": "Khomidok", "address": "Mini Secretariat Rd, Imphal, Khomidok, Manipur 795010", "district": "Imphal West"},
    {"name": "Jiribam Police Station", "code": "JRPS", "area": "Jiribam", "address": "Jiribam, Manipur 795116", "district": "Jiribam"},
    {"name": "Tungjoy Police Station", "code": "TJPS", "area": "Tungjoy", "address": "Tungjoy, Manipur 795104", "district": "Churachandpur"},
    {"name": "Lamsang Police Station", "code": "LSPS", "area": "Haorang Sabal", "address": "Haorang Sabal, Manipur 795113", "district": "Imphal West"},
    {"name": "Thoubal Police Station", "code": "TBPS", "area": "Thoubal", "address": "Thoubal Achouba, Thoubal, Manipur 795138", "district": "Thoubal"},
    {"name": "Kombiron Police Out Post", "code": "KBOP", "area": "Kombiron Village", "address": "Manipur Rd, Kombiron Village, Manipur 795147", "district": "Ukhrul"},
    {"name": "Longa Koireng Police Out Post", "code": "LKOP", "area": "Keithelmanbi", "address": "New Keithelmanbi, Longa Koireng, Manipur 795146", "district": "Senapati"},
    {"name": "Nongpok Sekmai Police Station", "code": "NSPS", "area": "Nongpok Sekmai", "address": "Nongpok Sekmai, Manipur 795149", "district": "Imphal East"},
    {"name": "Kakching Police Station", "code": "KCPS", "area": "Sugnu-Imphal Rd", "address": "KMC Road, Sugnu-Imphal Rd, Kakching, Manipur 795103", "district": "Kakching"},
    {"name": "Shangshak Police Station", "code": "SSPS", "area": "Kakching", "address": "Shangshak Khunou, Manipur 795145", "district": "Ukhrul"},
    {"name": "Cyber Crime Police Station", "code": "CCPS", "area": "Ragailong", "address": "Ragailong, Imphal, Kairang Meitei, Manipur 795001", "district": "Imphal West"},
    {"name": "Ngariyan Police Outpost", "code": "NGOP", "area": "Pinewood Garden Rd", "address": "Pinewood Garden Rd, Huikap, Manipur 795149", "district": "Imphal East"},
    {"name": "Chingmeirong Police Outpost", "code": "CMOP", "area": "Chingmeirong", "address": "Chingmeirong, Imphal, Heingang, Manipur 795010", "district": "Imphal East"},
    {"name": "Henglep Police Station", "code": "HLPS", "area": "Vongmoul", "address": "Vongmoul, Manipur 795128", "district": "Churachandpur"},
    {"name": "Maphou Police Station", "code": "MHPS", "area": "Nongdam", "address": "Nongdam Tangkhul, Manipur 795145", "district": "Ukhrul"},
    {"name": "Tentha Police Station", "code": "TNPS", "area": "Tentha", "address": "Tentha Khunou, Tentha, Manipur 795148", "district": "Tengnoupal"},
    {"name": "NK Manbi Police Station", "code": "NKPS", "area": "New Keithelmanbi", "address": "New Keithelmanbi, Longa Koireng, Manipur 795113", "district": "Senapati"},
    {"name": "Lilong Police Station", "code": "LLPS2", "area": "Lilong Khunou", "address": "Lilong Khunou, Takhok Makha, Lilong Chajing, Manipur 795130", "district": "Thoubal"},
    {"name": "Wangoo Police Station", "code": "WGPS", "area": "Wangoo", "address": "Wangoo, Wangoo Ahallup, Manipur 795103", "district": "Kakching"},
    {"name": "Litan Police Station", "code": "LTPS", "area": "Shangkai", "address": "Litan Police Station, Litan Shareikhong, Shangkai, Manipur 795145", "district": "Ukhrul"},
    {"name": "Purul Police Station", "code": "PRPS", "area": "Purul Road", "address": "Purul Road, Manipur 795015", "district": "Senapati"},
    {"name": "Nungba Police Station", "code": "NBPS", "area": "Nungba", "address": "Nungba, Manipur 795147", "district": "Tamenglong"},
    {"name": "Nambol Police Station", "code": "NMPS", "area": "Nambol", "address": "Laitonjam Khori Leikai, Nambol, Manipur 795134", "district": "Bishnupur"},
    {"name": "Khongsang Police Station", "code": "KSPS", "area": "Tamenglong", "address": "Tamenglong, Manipur 795159", "district": "Tamenglong"},
    {"name": "Serou Police Station", "code": "SRPS", "area": "Chakpikarong Road", "address": "Chandel - Chakpikarong Rd, Sugnu, Serou, Manipur 795101", "district": "Chandel"},
    {"name": "Lamsang Police Outpost", "code": "LSOP", "area": "Imphal", "address": "Imphal, Manipur 795113", "district": "Imphal West"},
    {"name": "Kangvai Police Outpost", "code": "KVOP", "area": "Kangvai", "address": "Kangvai, Manipur 795128", "district": "Churachandpur"},
    {"name": "Sekmaijin Police Out Post", "code": "SJOP", "area": "Sekmaijin Bridge", "address": "Sekmaijin Bridge, Hayel, Wabagai, Manipur 795103", "district": "Thoubal"},
    {"name": "Gamnom Saparmeina Police Station", "code": "GSPS", "area": "Saparmeina", "address": "Saparmeina, Manipur", "district": "Tamenglong"}
]

def add_stations():
    """Add all police stations to the database"""
    with app.app_context():
        print("Starting to add police stations...")
        
        added = 0
        updated = 0
        skipped = 0
        
        for station_data in stations_data:
            try:
                # Check if station already exists
                existing = mongo.db.stations.find_one({'code': station_data['code']})
                
                if existing:
                    # Update existing station
                    mongo.db.stations.update_one(
                        {'code': station_data['code']},
                        {'$set': {
                            'name': station_data['name'],
                            'area': station_data.get('area', ''),
                            'address': station_data.get('address', ''),
                            'district': station_data.get('district', ''),
                            'is_active': True,
                            'updated_at': datetime.utcnow()
                        }}
                    )
                    updated += 1
                    print(f"✓ Updated: {station_data['name']} ({station_data['code']})")
                else:
                    # Add new station
                    station_doc = {
                        'name': station_data['name'],
                        'code': station_data['code'],
                        'area': station_data.get('area', ''),
                        'address': station_data.get('address', ''),
                        'district': station_data.get('district', ''),
                        'type': 'Police Station',
                        'capacity': 50,
                        'is_active': True,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                    mongo.db.stations.insert_one(station_doc)
                    added += 1
                    print(f"✓ Added: {station_data['name']} ({station_data['code']})")
                    
            except Exception as e:
                print(f"✗ Error with {station_data.get('name', 'Unknown')}: {str(e)}")
                skipped += 1
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Added: {added}")
        print(f"  Updated: {updated}")
        print(f"  Skipped: {skipped}")
        print(f"  Total stations in database: {mongo.db.stations.count_documents({})}")
        print(f"{'='*60}")

if __name__ == "__main__":
    add_stations()
