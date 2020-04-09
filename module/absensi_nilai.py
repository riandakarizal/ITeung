from module import kelas
from lib import wa, reply
import config, os

def auth(data):
    if kelas.isParent(data[0]):
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num = data[0]
    studentid=kelas.getStudentIdFromParentPhoneNumber(num)
    scores=kelas.getStudentScores(studentid=studentid)
    studentname=scores[0][1]
    npm='NPM: '+studentid+'\n'
    nama='Nama: '+studentname+'\n'
    jadwalid=[]
    score='\n=====NILAI=====\n'
    for v in scores:
        jadwalid.append(v[-3])
        score=score+v[-2]+': '+v[-1]+'\n'
    absent='\n=====ABSENSI=====\n'
    for v in jadwalid:
        absent=absent+kelas.getDataMatkul(v)[1]+': '+str(round(int(kelas.getKehadiranMahasiswa(jadwalid=v, studentid=studentid)/config.kehadiran*100)))+'%\n'
    msgreply = npm + nama + score + absent
    return msgreply