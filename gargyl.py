"""
                *~ Pokus expansion 1.3 ~*
                           av
                   Gaute Svanes Lunde
"""
#Start med å importere alle de nødvendige delfilene.
from klasser import *
from grafikk import *
from quests import *
from prosedyrer import *

#Mainloop:
def gargyl_loop(spiller, inv, klasser, spellbook):
    qlog = klasser.questlog(4)
    vassleQlog = klasser.questlog(5)

    ferdig = False
    if not qlog.hent_quest(0).ferdig():
        ferdig = intro_loop(spiller, inv, klasser, spellbook)

    while not ferdig:
        garg_kart(qlog)

        valg = False
        quest = False
        gaaTilButikk = False
        fangekjeller = False
        utkikk = False
        while not valg:
            inn = input("Hvor vil du gå?\n> ").lower()

            if inn == "f":
                valg = True
                ferdig = True

            if inn == "q":
                quest = True
                valg = True

            if inn == "k":
                gaaTilButikk = True
                valg = True

            if inn == "s":
                ferdig = slottsgaard_loop(spiller, inv, klasser, spellbook)
                valg = True

            if inn == "a" and qlog.hent_quest(1).startet():
                fangekjeller = True
                valg = True

            if inn == "u" and qlog.hent_quest(2).startet():
                utkikk = True
                valg = True

        while quest:
            #Merk at oppdrag_tilgjengelige() er en funksjon med returverdi.
            inn = qlog.oppdrag_tilgjengelige(spiller.lvl(), "møtehallen").lower()
            if inn != "f" and inn != "ferdig":
                try:
                    qlog.snakk(int(inn) - 1, spiller, inv)
                except ValueError:
                    print("\nDu må skrive et tall!\n")
            else:
                quest = False

            #oppdaterer vasslequests
            if qlog.hent_quest(5).ferdig():
                vassleQlog.hent_quest(2).progresser()

        while gaaTilButikk:
            klasser.butikk(3).interaksjon(inv)
            gaaTilButikk = False

        fiender = 0
        while fangekjeller:

            if not angrip(spiller, generer_statue(spiller), inv, klasser, spellbook):
                fangekjeller = False
                break
            fiender += 1

            if fiender > randint(5, 8):
                print(spiller.navn(), "har nådd bunnen av fangekjelleren, og har funnet en mystisk kiste!")

                if not qlog.hent_quest(1).ferdig():
                    qlog.hent_quest(1).progresser()
                    print(spiller.navn(), "fant noen gamle, uforståelige skrifter i kisten.")

                    #bq1
                    if randint(0, 10) > 7 and qlog.hent_quest(6).progresjon() == 0:
                        qlog.hent_quest(6).progresser()
                        print(spiller.navn(), "fant en levende kosebamse i kisten! Hvem kan det være sin?")

                    input("Trykk enter for å dra tilbake\n> ")
                    fangekjeller = False
                else:
                    loot = Loot()
                    ormLoot(loot)
                    fiende = Fiende("Orm", "dyr", loot, 2300, 150, 130, ending="en")
                    print("\nEn svær orm gjemte seg i kisten!\n" + spiller.navn(), "har møtt en orm!")
                    if angrip(spiller, fiende, inv, klasser, spellbook):
                        print("\n" + spiller.navn(), "fant 350 gullstykker, en stripe konsentrasjonspulver og en trolldrikk i kisten.")
                        item = Item("Trolldrikk", "restoring", hp=300)
                        inv.legg_til_item(item)
                        item = Item("Konsentrasjonspulver", "restoring", kp=200)
                        inv.legg_til_item(item)
                        inv.penger(350)

                        #bq1
                        if randint(0, 10) > 6 and qlog.hent_quest(6).progresjon() == 0:
                            qlog.hent_quest(6).progresser()
                            print(spiller.navn(), "fant en levende kosebamse i kisten! Hvem kan det være sin?")

                        input("Trykk enter for å dra tilbake\n> ")
                    fangekjeller = False
            else:
                print("\n" + spiller.navn(), "går dypere ned i fangekjelleren.")
                input("Trykk enter for å fortsette\n> ")

        while utkikk:
            if not qlog.hent_quest(2).ferdig():
                qlog.hent_quest(2).progresser()
                angrip(spiller, generer_gargyl(spiller), inv, klasser, spellbook)
                utkikk = False
            else:
                tall = randint(1, 10)
                if tall <= 7:
                    fiende = generer_gargyl(spiller)
                else:
                    fiende = generer_statue(spiller)
                if not angrip(spiller, fiende, inv, klasser, spellbook):
                    utikk = False
                    break
                if fiende.race() == "gargyl":
                    qlog.hent_quest(5).progresser()
                if qlog.hent_quest(5).progresjon() == 7 and not qlog.hent_quest(5).ferdig():
                    guri_dialog(spiller)
                    loot = Loot()
                    guriLoot(loot)
                    fiende = Fiende("Guri Gargyl", "gargyl", loot, 7000, 400, 250, kp=300, bonusKp=7, weapon=70)
                    if angrip(spiller, fiende, inv, klasser, spellbook):
                        qlog.hent_quest(5).progresser_liste(0)
                        utkikk = False

    if ferdig:
        return verdenskart(spiller)

def intro_loop(spiller, inv, klasser, spellbook):

    print("\n    "+spiller.navn(), """kommer til et mørkt og dystert slott! Store steiner ligger
    strødt rundt omkring. Den nærmeste begynner å bevege på seg, og
    sakte flyr rundt i sirkel, før den suser rett mot""", spiller.navn()+"!\n")
    input("Trykk enter for å fortsette\n> ")

    skrivStein()
    print(spiller.navn(), "har møtt en stein!")
    fiende = Fiende("Stein", "objekt", Loot(), hp=300, a=130, d=100, weapon=60)
    fiende.return_loot().legg_til_item(50, 100)

    angrip(spiller, fiende, inv, klasser, spellbook)

    return slottsgaard_loop(spiller, inv, klasser, spellbook)

def slottsgaard_loop(spiller, inv, klasser, spellbook):
    qlog = klasser.questlog(4)
    while True:
        intro_kart(qlog)
        inn = input("\nHvor vil du dra?\n> ").lower()

        if inn == "q" and not qlog.hent_quest(0).ferdig():
            qlog.snakk(0, spiller, inv)

        if inn == "q" and qlog.hent_quest(3).startet() and not qlog.hent_quest(4).ferdig():
            qlog.hent_quest(4).sett_tilgjengelig()
            qlog.snakk(4, spiller, inv)
            qlog.hent_quest(4).sett_tilgjengelig(False)
            qlog.hent_quest(3).progresser()
            if qlog.hent_quest(4).ferdig():
                qlog.hent_quest(3).progresser_liste(0)

        if inn == "s":
            while True:
                skrivStein()
                fiende = Fiende("Stein", "objekt", Loot(), hp=300, a=130, d=100, weapon=60)
                fiende.return_loot().legg_til_item(70, 100)
                print(spiller.navn(), "har møtt en stein!")

                if not angrip(spiller, fiende, inv, klasser, spellbook):
                    break
                if qlog.hent_quest(0).startet():
                    qlog.hent_quest(0).progresser()
                if qlog.hent_quest(4).startet():
                    qlog.hent_quest(4).progresser()

        if inn == "f":
            return True

        if inn == "t" and qlog.hent_quest(0).ferdig():
            return False

def angrip(spiller, fiende, inv, klasser, spellbook):
    qlog = klasser.questlog(4)
    skriv_ut(spiller, fiende)
    tur = True
    while True:
        inn = input("\nHva vil du gjøre?\n> ").lower()

        if inn == "f" or inn == "flykt":
            print(spiller.navn(), "drar tilbake til slottsgården.")
            return False

        tur = kommandoer(inn, spiller, fiende, inv, klasser, spellbook)

        #Her sjekkes om fienden er død. Om så, får karakteren loot og xp.
        if fiende.dead():
            print("--------------------------------------------------------------------"+\
            "\nDu vant!", fiende.navn() + fiende.ending(), "er overvunnet!",spiller.navn(),"får",fiende.xp(),"erfaringspoeng.")
            spiller.kons()
            spiller.gi_xp(fiende.xp())
            fiende.loot(spiller, inv)
            input("Trykk enter for å fortsette\n> ")
            return True

        elif not tur:
            if fiende.race() == "gargyl" and fiende.kp() >= 100 and randint(0, 1) == 1 and fiende.untouchableCD() >= 0:
                print(fiende.navn() + fiende.ending(), "kastet RockNoRoll!")
                print(fiende.navn() + fiende.ending(), "er blitt til stein!")
                fiende.bruk_kons(100)
                fiende.set_untouchable(True, 10)
            elif fiende.race() != "gargyl" and fiende.kp() >= 50 and randint(0, 2) == 1 \
            and fiende.xHp() - fiende.hp() > 80:
                print(fiende.navn() + fiende.ending(), "kastet restituer!")
                print(fiende.navn() + fiende.ending(), "restorerte", fiende.restorer(100), "hp!")
                fiende.bruk_kons(50)
            elif fiende.race() == "gargyl" and fiende.kp() >= 40 and randint(0, 10) == 1 \
            and fiende.xHp() - fiende.hp() > 100:
                print(fiende.navn() + fiende.ending(), "kastet restituer!")
                print(fiende.navn() + fiende.ending(), "restorerte", fiende.restorer(100), "hp!")
                fiende.bruk_kons(40)
            else:
                spiller.angrepet(fiende)

            #gir beskjed om karakteren døde
            if spiller.dead():
                write_player_died(spiller, "slottet")
                player_died(spiller, inv, klasser)
                return False

            #skriver ut hp og kp til karakteren og hp til fienden til neste runde.
            else:
                spiller.kons()
                fiende.gen_kons()
                skriv_ut(spiller, fiende)

def generer_statue(spiller):
    loot = Loot()
    fiende = Fiende(navn="Statue", race="objekt", loot=loot, \
    hp=60 + 20 * randint(1, spiller.lvl()), \
    a=20 + randint(0, 10 * spiller.lvl()), \
    d=30 + randint(0, 10 * spiller.lvl()), \
    kp=50 + randint(0, 3 * spiller.lvl()), bonusKp=2, ending="n")
    dynamiskLoot(loot, fiende, spiller)
    skrivStatue()
    print("\n" + spiller.navn(), "har møtt på en levende statue!")
    return fiende

def generer_gargyl(spiller):
    loot = Loot()
    hp = 1000 + randint(0, spiller.lvl()) * 25
    a = 180 + randint(spiller.lvl() - 10, spiller.lvl() + 10)
    d = 120 + 2 * spiller.lvl()
    kp = 130 + 5 * round(spiller.lvl() / 4) + randint(-10, 10)
    bkp = randint(4, 6)
    w = randint(65, 75)
    fiende = Fiende("Gargyl", "gargyl", loot, hp, a, d, kp=kp, bonusKp=bkp, weapon=w, ending="en")
    gargylLoot(loot, fiende, spiller)
    skrivGargouille()
    print("\n" + spiller.navn(), "har møtt på en gargyl!")
    return fiende

def dynamiskLoot(loot, fiende, spiller):
    tall = round(10 + fiende.xp() / 10)
    loot.legg_til_item(tall, 60)

    kpkp = int(randint(1, spiller.lvl()) /10) *25 + 100
    item = Item("Konsentrasjonspulver", "restoring", kp=kpkp)
    item.sett_loot_tekst("en stripe konsentrasjonspulver")
    loot.legg_til_item(item, 10)

    tdhp = randint(1, spiller.lvl()) * 5 + 175
    item = Item("Trolldrikk", "restoring", hp=tdhp)
    loot.legg_til_item(item, 15)

    a = randint(0, 4 * spiller.lvl())
    xKp = randint(0, 3 * spiller.lvl())
    item = Item("Stiv stav", "weapon", a=a, xKp=xKp)
    loot.legg_til_item(item, 5)

    a = randint(40, 40 + 5 * spiller.lvl())
    item = Item("Sverd'I'stein", "weapon", a=a, blade=True)
    item.sett_loot_tekst("et sverd")
    loot.legg_til_item(item, 6)

    xHp = randint(0, 2 * spiller.lvl())
    d = int(randint(0, 4 * spiller.lvl()) /10) *10
    item = Item("Rusten rustning", "robe", xHp=xHp, d=d)
    loot.legg_til_item(item, 4)

def ormLoot(loot):
    item = Item("Ormeskinn:Pannebånd", "hat", xHp=70, d=60)
    loot.legg_til_item(item, 20)

    item = Item("Ormeskinn:Sko", "shoes", xHp=20, xKp=30, a=10)
    loot.legg_til_item(item, 20)

    item = Item("Ormeskinn:Truse", "robe", xKp=100)
    loot.legg_til_item(item, 20)

    item = Item("Ormeskinn:Hansker", "gloves", a=10, xHp=10, xKp=10)
    loot.legg_til_item(item, 20)

    item = Item("Ormetann", "weapon", a=135, xHp=15, blade=True)
    loot.legg_til_item(item, 20)

def gargylLoot(loot, fiende, spiller):
    tall = round(30 + fiende.xp() / 10)
    loot.legg_til_item(tall, 60)

    kpkp = int(randint(1, spiller.lvl()) /10) *25 + 100
    item = Item("Konsentrasjonspulver", "restoring", kp=kpkp)
    item.sett_loot_tekst("en stripe konsentrasjonspulver")
    loot.legg_til_item(item, 10)

    tdhp = randint(1, spiller.lvl()) * 5 + 175
    item = Item("Trolldrikk", "restoring", hp=tdhp)
    loot.legg_til_item(item, 15)

    hp = randint(0, 4) * 10
    kp = randint(1, 5) * 10
    ekp = randint(1, 4)
    item = Item("Stein", "trinket", xHp=hp, kp=kp, ekstraKp=ekp)
    loot.legg_til_item(item, 5)

def guriLoot(loot):
    loot.legg_til_item(2000, 25)

    item = Item("Steinsko", "shoes", xHp=-30, d=100, lvl=19)
    item.sett_loot_tekst("et par sko av stein")
    loot.legg_til_item(item, 25)

    item = Item("Stein-hatt", "hat", xHp=-30, d=125, lvl=19)
    loot.legg_til_item(item, 25)

    item = Item("Krystallkule", "trinket", xHp=125, lvl=19)
    loot.legg_til_item(item, 25)

def garg_kart(qlog):
    skrivGargylslott()
    print("""
    Velkommen til slottet! Her er stedene du kan dra:
    Slottsgården (s)           Dra til slottsgården
    Butikken (k)               Se hva Tina har tilgjengelig i 'Skattekammeret'
    Møtehallen (q)             Diskuter angrepsstrategi i møtehallen""")
    if qlog.hent_qLog()[1].startet():
        print("    Fangekjelleren (a)         Dra til fangekjelleren og finn skjulte skatter!")
    if qlog.hent_qLog()[2].startet():
        print("    Utkikkstårnet (u)          Bekjemp gargyler i de øvre delene av slottet!")
    print("    Ut i verden (f)            Viser deg kart over alle stedene du kan dra\n")

def intro_kart(qlog):
    print("""
    Du står i slottsgården! Her er stedene du kan dra:
    Slottsporten (s)           Rydd bort steiner foran slottsporten""")
    if not qlog.hent_quest(0).ferdig():
        print("    Fontenen (q)               Snakk med Zap")
    if qlog.hent_quest(3).startet() and not qlog.hent_quest(4).ferdig():
        print("    Fontenen (q)               Snakk med Kent Kokk")
    if qlog.hent_quest(0).ferdig():
        print("    Slottet (t)                Dra til slottet")
    print("    Verdenskart (f)            Se på verdenskartet")

def garg_butikk(butikk):
    butikk.legg_til_hadeTekst("\nVelkommen tilbake! Og se opp for gangster-fiskene!\n")

    item = Item("Tryllepulver", "damaging", dmg=100)
    vare = Vare(item, 50, "t")
    butikk.legg_til_vare(vare)

    item = Item("Trolldrikk", "restoring", hp=300)
    vare = Vare(item, 400, "d")
    butikk.legg_til_vare(vare)

    item = Item("Konsentrasjonspulver", "restoring", kp=150)
    vare = Vare(item, 500, "k")
    butikk.legg_til_vare(vare)

    item = Item("Tryllestav", "weapon", a=60, xKp=45)
    vare = Vare(item, 1000, "w")
    butikk.legg_til_vare(vare)

    item = Item("Sverd", "weapon", a=100, xHp=20, blade=True)
    vare = Vare(item, 3000, "v")
    butikk.legg_til_vare(vare)

    item = Item("falskt skjegg", "beard", xKp=30, ekstraKp=3)
    vare = Vare(item, 1100, "g")
    butikk.legg_til_vare(vare)

def garg_quest(qlog, spiller):
    navn = spiller.navn()

    #q1
    desk1 = garg_q1(navn)
    ferdigDesk1 = garg_q1_ferdig(navn)
    q1 = Quest(desk1, ferdigDesk1, 7, 15, "Zap")
    q1.legg_til_reward(xp=2000, gull=300)
    q1.legg_til_progresjonTekst("Steiner ryddet: ")
    q1.legg_til_svarTekst("\nKan jeg regne med din hjelp?     (ja/nei)\n> ")
    qlog.legg_til_quest(q1)

    #q2
    desk2 = garg_q2(navn)
    ferdigDesk2 = garg_q2_ferdig(navn)
    q2 = Quest(desk2, ferdigDesk2, 1, 15, "Zap")
    q2.legg_til_reward(xp=4000, gull=500, settTilgjengelig=True, settTilgjengeligIndeks=2)
    q2.legg_til_progresjonTekst("Logg funnet: ")
    q2.legg_til_svarTekst("\nVil du hjelpe?    (ja/nei)\n> ")
    qlog.legg_til_quest(q2)

    #q3
    desk3 = garg_q3(navn)
    ferdigDesk3 = garg_q3_ferdig(navn)
    q3 = Quest(desk3, ferdigDesk3, 1, 16, "Zap", tilgjengelig=False)
    q3.legg_til_reward(xp=1000, hp=10, settTilgjengelig=True, settTilgjengeligIndeks=3)
    q3.legg_til_progresjonTekst("Utkikkstårn utforsket: ")
    q3.legg_til_svarTekst("\nVil du hjelpe?    (ja/nei)\n> ")
    qlog.legg_til_quest(q3)

    #q4
    desk4 = garg_q4(navn)
    ferdigDesk4 = garg_q4_ferdig(navn)
    q4 = Quest(desk4, ferdigDesk4, 1, 16, "Zap", tilgjengelig=False)
    q4.legg_til_reward(xp=6500, gull=1000, kp=20, settTilgjengelig=True, settTilgjengeligIndeks=5)
    q4.legg_til_progresjonTekst("Kent Kokk snakket med: ")
    q4.legg_til_progresjon(1)
    q4.legg_til_progresjonTekstListe("Trylleformel lært: ", 0)
    q4.legg_til_svarTekst("\nVil du hjelpe oss?    (ja/nei)\n> ")
    qlog.legg_til_quest(q4)

    #q5
    desk5 = garg_q5(navn)
    ferdigDesk5 = garg_q5_ferdig(navn)
    q5 = Quest(desk5, ferdigDesk5, 10, 16, "Kent Kokk", tilgjengelig=False, resetIfDead=True)
    q5.legg_til_reward(xp=2500, gull=100)
    q5.legg_til_progresjonTekst("Steiner samlet inn: ")
    q5.legg_til_ekstra_tekst("Du har lært et nytt trylletriks, 'kjøttifiser' ('kj')!")
    q5.legg_til_svarTekst("\nVil du hjelpe oss?    (ja/nei)\n> ")
    qlog.legg_til_quest(q5)

    #q6
    desk6 = garg_q6(navn)
    ferdigDesk6 = garg_q6_ferdig(navn)
    q6 = Quest(desk6, ferdigDesk6, 7, 17, "Zap", tilgjengelig=False)
    q6.legg_til_reward(xp=10000, gull=1000, hp=50, kp=20, ekstraKp=1)
    q6.legg_til_progresjonTekst("Gargyler tillintetgjort: ")
    q6.legg_til_progresjon(1)
    q6.legg_til_progresjonTekstListe("Guri Gargyl slaktet: ", 0)
    q6.legg_til_svarTekst("\nVil du hjelpe oss?    (ja/nei)\n> ")
    qlog.legg_til_quest(q6)

    #bq1
    deskBq1 = garg_bq1(navn)
    ferdigDeskBq1 = garg_bq1_ferdig(navn)
    bq1 = Quest(deskBq1, ferdigDeskBq1, 1, 1, "Besynderlige Berit", bonus=True, resetIfDead=True)
    item = Item("Berits skjegg", "beard", kp=50, ekstraKp=5)
    bq1.legg_til_reward(xp=10000, item=item)
    bq1.legg_til_ekstra_tekst("Dette betyr så mye for oss! Her, ta det magiske skjegget mitt!.\n")
    bq1.legg_til_progresjonTekst("Kosebamse funnet: ")
    bq1.legg_til_svarTekst("Vil du gi kosebamsen til Besynderlige Berit?   (ja/nei)\n> ")
    qlog.legg_til_quest(bq1)

def guri_dialog(spiller):
    navn = spiller.navn()
    print("\n\n    ***", spiller.navn(), "har møtt Guri Gargyl! ***\n\n")
    skrivGuri()
    input("Trykk enter for å fortsette\n> ")
    print("""
    Guri Gargyl: Så det er du som har kjøttifisert kreasjonene mine!
                 Dette ender nå! Jeg fikk ikke magiske evner og et så
                 stort ansvar og bare for å miste det hele til et usselt
                 menneske. Forbered deg på det verste,""", navn + "!\n")
    input("Trykk enter for å fortsette\n> ")
