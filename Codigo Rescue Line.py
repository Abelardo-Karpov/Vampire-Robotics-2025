import sensor, image, time
from motors import move
from pyb import Pin
#ajustes de inicio
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.set_auto_exposure(False)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.skip_frames(time = 2000)


def rodearR():
    move(0,0)
    time.sleep(0.4)
    move(-30,-30)
    time.sleep(0.3)
    move(60,-60)
    time.sleep(0.6)
    move(0,100)
    time.sleep(1.8)
    move(60,-60)
    time.sleep(0.8)
    move(-40,-40)
    time.sleep(0.5)
def rodearL():
    move(0,0)
    time.sleep(0.4)
    move(-30,-30)
    time.sleep(0.3)
    move(-60,60)
    time.sleep(0.6)
    move(100,9)
    time.sleep(2.10)
    move(-60,60)
    time.sleep(0.7)
    move(-40,-40)
    time.sleep(0.6)
def rodearRcuarto():
    move(0,0)
    time.sleep(0.4)
    move(-30,-30)
    time.sleep(0.2)
    move(60,-60)
    time.sleep(0.7)
    move(0,100)
    time.sleep(1.2)
    move(60,-60)
    time.sleep(0.7)
    move(-40,-40)
    time.sleep(0.5)
def rodearLcuarto():
    move(0,0)
    time.sleep(0.4)
    move(-30,-30)
    time.sleep(0.2)
    move(-60,60)
    time.sleep(0.7)
    move(100,10)
    time.sleep(1)
    move(-60,60)
    time.sleep(0.7)
    move(-40,-40)
    time.sleep(0.5)


pin0 = Pin("P0", Pin.IN, Pin.PULL_UP)
pin1 = Pin("P1", Pin.OUT_PP, Pin.PULL_NONE)
pin2 = Pin("P2", Pin.IN, Pin.PULL_UP)
pin3 = Pin("P3", Pin.OUT_PP, Pin.PULL_NONE)
cverde=[(48, 96, -55, -21, -19, 8)]
cnegro=[(65, 0, -16, 5, -20, 8)]
cnegro2=[(0, 68, -21, 11, -22, 9)]
crojo=[(36, 74, 7, 55, -7, 49)]
verde=0
vel=50
m1=0
m2=0
Dif=0
while True:
    img = sensor.snapshot()
    negro = img.find_blobs(cnegro, area_threshold=300,roi=(0,0,160,30))
    #SEGUIMIENTO DE LINEA
    if negro:
        negro = max(negro, key=lambda b: b.pixels())
        img.draw_rectangle(negro.x(),negro.y(),negro.w(),1, (255,0,0), 4, False)
        error=abs(80-negro.cx())
        kp=vel/40
        arreglo=error*kp*1.85

        #m1 = vel - arreglo if negro.cx()<80 else vel
        #m2 = vel if negro.cx()<80 else vel - arreglo
        if negro.cx()<80:
            m1=vel-arreglo
            m2=vel
        else:
            m1=vel
            m2=vel-arreglo

        move(m1, m2)

    else:
        negroL = img.find_blobs(cnegro, area_threshold=300, roi=(0,0,12,100))
        if negroL:
            negroL = max(negroL, key=lambda b: b.pixels())
            img.draw_rectangle(negroL.rect(), (255,255,0), 4, False)
            print("NEGRO IZQUIERDA")
            move(-vel,vel)
            time.sleep(0.55)
        else:
            negroR = img.find_blobs(cnegro, area_threshold=300, roi=(148,0,12,100))
            if negroR:
                negroR = max(negroR, key=lambda b: b.pixels())
                img.draw_rectangle(negroR.rect(), (255,255,0), 4, False)
                print("NEGRO DERECHA")
                move(vel,-vel)
                time.sleep(0.55)

    #DETECCION VERDES
    if negro:
        if negro.w() > 90:
            cantidad=0
            for verde in img.find_blobs(cverde, area_threshold=250, roi= (25,0,110,60)):
                img.draw_rectangle(verde.x(), verde.y(), verde.w(), verde.h(), (0,200,0), 4, False)
                if verde.cy() > negro.cy():
                    cantidad=cantidad+1
                img.draw_string(verde.x(), verde.y(), str(cantidad))
            if verde:
                if verde.y()>=30:
                    if cantidad == 1:
                        negro2 = img.find_blobs(cnegro2, area_threshold=150, roi=(0,30,160,30))
                        if negro2:
                            negro2 = max(negro2, key=lambda b: b.pixels())
                            img.draw_rectangle(negro2.x(), negro2.y(), negro2.w(), negro2.h(), (255,100,0), 4, False)
                            if verde.cx() < negro2.cx():
                                print("giro verde I")
                                move(-60,60)
                                time.sleep(0.65)
                            else:
                                print("Giro verde D")
                                move(60,-60)
                                time.sleep(0.65)
                    elif cantidad == 2:
                        print("Giro retornar")
                        move(60,-60)
                        time.sleep(1.3)
    # Obstaculo
    if pin0.value() == 0:
        autoObs()
    #Deteccion rojo
    #rojo = img.find_blobs(crojo, area_threshold=150,roi=(0,10,160,40))
    #if rojo:
    #    rojo = max(rojo, key=lambda b: b.pixels())
    #    img.draw_rectangle(rojo.rect(), (255,255,0), 4, False)
    #    move(0,0)
    #    time.sleep(5)
    #    move(25,25)
    #    time.sleep(0.3)

        move(60,60)
        time.sleep(1.25)
        move(60,-60)
        time.sleep(0.8)
        move(60,60)
        time.sleep(0.4)
    #Correccion no linea
    negromid = img.find_blobs(cnegro, area_threshold=300, roi=(0,45,160,45))
    if negro and negromid:
        negromid = max(negromid, key=lambda b: b.pixels())
        img.draw_rectangle(negromid.x(), negromid.y(), negromid.w(), negromid.h(), (255,100,0), 4, False)
        print("negromid detectado:" + " " + str(negromid.cx()))
        Dif = negromid.cx() - negro.cx()
        print("Diferencia entre negromid y negroprincipal:" + " " + str(Dif))

    if not negro:
        print(Dif)
        if Dif<0:
            Dif+=1
            move(60,-60)
        if Dif>0:
            Dif-=1
            move(-60,60)
        if Dif==0:
            move(50,50)






