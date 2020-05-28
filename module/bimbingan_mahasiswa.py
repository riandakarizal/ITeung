from lib import wa, reply, message
from module import kelas
from Crypto.Cipher import AES
from datetime import datetime
import os, config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msg=data[3]
    msg=message.normalize(msg)
    tipe_bimbingan=msg.split('bimbingan ')[1].split(' topik')[0]
    studentid=kelas.getNpmandNameMahasiswa(data[0])[0]
    topik=msg.split('topik ')[1].split(' nilai')[0].replace(' ', '%20')
    # pertemuan=msg.split('pertemuan ')[1].split(' nilai')[0]
    target_selesai = msg.split('target selesai ')[1].split(' target selanjutnya')[0]
    terget_selanjutnya = msg.split('target selanjutnya ')[1].split(' nilai')[0]
    nilai=msg.split('nilai ')[1]
    datenow = datetime.date(datetime.now()).strftime('%d%m%Y')
    hari = datetime.now().strftime('%A')
    hari = hariSwitcher(hari)
    obj = AES.new(config.key, AES.MODE_CBC, config.iv)
    cp = obj.encrypt(studentid+datenow+hari)
    passcode=cp.hex()
    msgreply='https://api.whatsapp.com/send?phone={nomoriteung}&text=iteung%20input%20bimbingan%20{tipebimbingan}%20{npm}%0Atopik%20{topikbimbingan}%0Atarget%20selesai%20{targetselesai}%0Atarget%20selanjutnya%20{targetselanjutnya}%0Anilai%20{nilai}%0Apasscode%20{passcode}'.format(
        nomoriteung=config.nomor_iteung,
        tipebimbingan=tipe_bimbingan,
        npm=studentid,
        topikbimbingan=topik,
        nilai=nilai,
        passcode=passcode,
        targetselesai=target_selesai,
        targetselanjutnya=terget_selanjutnya
    )
    return msgreply

def hariSwitcher(hari):
    switcher = {
        'Monday': '1',
        'Tuesday': '2',
        'Wednesday': '3',
        'Thursday': '4',
        'Friday': '5',
        'Saturday': '6',
        'Sunday': '7',
    }
    return switcher.get(hari, 'days not found!')