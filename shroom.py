"""
                *~ Pokus expansion 2.0 ~*
                           av
                   Gaute Svanes Lunde
"""

from klasser import *
from grafikk import *
from quests import *
from prosedyrer import *

#Mainloop:
def shroom_loop(spiller, inv, klasser, spellbook):
    qlog = klasser.questlog(6)
    bQlog = klasser.questlog(7)
    vassleQlog = klasser.questlog(5)
    ferdig = False

    if not vassleQlog.hent_quest(3).progresjon():
        ferdig = intro_loop(spiller, inv, klasser, spellbook)

    while not ferdig:
        skog_kart(qlog)

        valg = False
        quest = False
        gaaTilButikk = False
        fight = False
        leirBaal = False
        lagre = False
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
                fight = True
                valg = True

            if inn == "l":
                lagre = True
                valg = True

            if inn == "b":
                leirBaal = True
                valg = True

        if leirBaal:
            leirBaal = False
            ferdig = sti(spiller, inv, klasser, spellbook)

        while quest:
            inn = qlog.oppdrag_tilgjengelige(spiller.lvl(), "strategi-teltet").lower()
            kjellQ = bQlog.hent_quest(5)
            if kjellQ.startet() and not kjellQ.ferdig() and inn == "3":
                if not kjellLoop(spiller, inv, klasser, spellbook, kjellQ):
                    quest = False
            elif inn != "f" and inn != "ferdig":
                try:
                    qlog.snakk(int(inn) - 1, spiller, inv)
                except ValueError:
                    print("\nDu må skrive et tall!\n")
            else:
                quest = False

        while gaaTilButikk:
            klasser.butikk(4).interaksjon(inv)
            gaaTilButikk = False

        while fight:
            if randint(1, 1) == 1:
                fiende = generer_guffsliffsaff(spiller)

            fight = angrip(spiller, fiende, inv, klasser, spellbook)

        while lagre:
            minnestein(spiller, inv, klasser)
            lagre = False

    if ferdig:
        return verdenskart(spiller)

def intro_loop(spiller, inv, klasser, spellbook):
    print("    **", spiller.navn(), """kommer til et utbrent leirbål. Det er blod på bakken, og
    spor etter kamp. Det virker ikke som om det er lenge siden noen var her,
    men det er vanskelig å si hvor de gikk. Hovedstien deler seg til høyre
    og venstre.
    """)

    input("Trykk enter for å fortsette\n> ")
    print("""\n*En banditt kommer løpende ut fra ingensteds*

    Banditt: Du er en av dem, er du ikke? Jeg skal finne dem! Jeg har fått
    torturert ut noen veibeskrivelser av en ynkelig rotte, og nå slipper
    ingen av dere unna! Og min enmanns-massakre starter med deg!\n""")

    if not angrip(spiller, generer_banditt(spiller), inv, klasser, spellbook):
        return True
    print("\n*" + spiller.navn() + "finner en lapp på banditten! På den står det:")
    print("\n    Hold høyre!\n\nForan deg har du to stier, og du må velge en.")

    return sti(spiller, inv, klasser, spellbook)

def sti(spiller, inv, klasser, spellbook):
    vassleQlog = klasser.questlog(5)
    shroomQlog = klasser.questlog(6)
    while True:
        #Sti 1
        print("\nStien deler seg")
        valg1 = input("Hvor vil du gå? (h/v)\n> ")
        while valg1.lower() not in {"h", "v", "høyre", "venstre"}:
            valg1 = input("Hvor vil du gå? Skriv 'høyre' eller 'venstre':\n> ")
        h1 = False
        tekst = spiller.navn() + " tar til venstre med første veideling\n"
        if valg1.lower() in {"h", "høyre"}:
            h1 = True
            tekst =  spiller.navn() + " tar til høyre med første veideling\n"
        print(tekst)
        if randint(1, 3) == 3 and not angrip(spiller, generer_banditt(spiller), inv, klasser, spellbook):
            return True

        #Sti 2
        print("Stien deler seg igjen.")
        valg2 = input("Hvor vil du gå? (h/v)\n> ")
        while valg2.lower() not in {"h", "v", "høyre", "venstre"}:
            valg2 = input("Hvor vil du gå? Skriv 'høyre' eller 'venstre':\n> ")
        h2 = False
        tekst = spiller.navn() + " tar til venstre med andre veideling\n"
        if valg2.lower() in {"h", "høyre"}:
            h2 = True
            tekst =  spiller.navn() + " tar til høyre med andre veideling\n"
        print(tekst)
        if randint(1, 3) == 3 and not angrip(spiller, generer_banditt(spiller), inv, klasser, spellbook):
            return True

        #Sti 3
        print("Stien deler seg igjen.")
        valg3 = input("Hvor vil du gå? (h/v)\n> ")
        while valg3.lower() not in {"h", "v", "høyre", "venstre"}:
            valg3 = input("Hvor vil du gå? Skriv 'høyre' eller 'venstre':\n> ")
        h3 = False
        tekst = spiller.navn() + " tar til venstre med tredje veideling\n"
        if valg3.lower() in {"h", "høyre"}:
            h3 = True
            tekst =  spiller.navn() + " tar til høyre med tredje veideling\n"
        print(tekst)
        if randint(1, 3) == 3 and not angrip(spiller, generer_banditt(spiller), inv, klasser, spellbook):
            return True

        if not h1 and not h2 and not h3:
            print("\n\n    **Du fant stien som fører til ekspedisjonsleiren!**\n\n")
            input("Trykk enter for å fortsette\n> ")
            vassleQlog.hent_quest(3).progresser()
            return False

        elif h1 and h2 and h3:
            print("""\n\n           **Du fant en avrevet side fra en gammel bok! På den står det:
            ---
             _  _  .-'   '-.
            (.)(.)/         \\
             /66            ;   jgs
            o_\\\\-mm-......-mm`~~~~~~~~~~~~~

            ...Rotter har en tendens til å glemme forskjellen på høyre og venstre
            når de blir utsatt for smerte. En som f.eks sier "hold høyre" mener
            da egentlig "hold venstre". En annen nyttig faktaopplysning omhandler...
            ---
            På en eller annen måte finner du veien tilbake til leirbålet du var med
            sist.**""")
        elif h1 and not h2 and h3:
            print("""\n\n        *Du fant et skilt hvor det står "BANDITT-LEIR"* """)
            if shroomQlog.hent_quest(0).startet():
                print("\nDu går inn til leiren.")
                input("\nTrykk enter for å fortsette\n> ")
                return banditt_loop(spiller, inv, klasser, spellbook)
            else:
                print("\nDet er ikke en banditt-leir", spiller.navn(), "er på jakt etter.")
                print("Du bestemmer deg for å dra tilbake til leirbålet.")
        elif not h1 and h2 and not h3 and shroomQlog.hent_quest(0).startet():
            print("Blindvei! Du får en følelse av at rotters stedsans ikke er helt bra.")
            print("Kanksje du kan prøve det motsatte? Du drar tilbake til leirbålet.")
        else:
            print("Blindvei! På en eller annen måte finner du veien tilbake til leirbålet.")

def banditt_loop(spiller, inv, klasser, spellbook):
    sQlog = klasser.questlog(6)
    bQlog = klasser.questlog(7)
    if not sQlog.hent_quest(0).ferdig():
        print(spiller.navn(), "har møtt en banditt!")
        print("Banditten tror", spiller.navn(), "også er en banditt.")
        print("Alle smiler til deg som en felles banditt, \nmen noe er ikke som det skal i leiren.")
        input("\nTrykk enter for å fortsette\n> ")

    ferdig = False
    while not ferdig:
        #skrivBandittLeir()
        banditt_kart(bQlog)

        valg = False
        quest = False
        gaaTilButikk = False
        skogen = False
        sopp = False
        duell = False
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

            if inn == "d":
                duell = True
                valg = True

            if inn == "s":
                skogen = True
                valg = True

            if inn == "p" and bQlog.hent_quest(2).startet():
                sopp = True
                valg = True

        while quest:
            inn = bQlog.oppdrag_tilgjengelige(spiller.lvl(), "stortreet").lower()
            if inn == "2" and bQlog.hent_quest(1).progresjon() == 6 and not bQlog.hent_quest(1).progresjon_liste()[0]:
                if not ussleUlvLoop(spiller, inv, klasser, spellbook):
                    inn = "f"
            if inn != "f" and inn != "ferdig":
                try:
                    bQlog.snakk(int(inn) - 1, spiller, inv)
                except ValueError:
                    print("\nDu må skrive et tall!\n")
            else:
                quest = False
            if bQlog.hent_quest(5).ferdig():
                sQlog.hent_quest(0).progresser()

        while gaaTilButikk:
            klasser.butikk(5).interaksjon(inv)
            gaaTilButikk = False

        while skogen:
            tall = randint(1, 10)
            if tall >= 6:
                fiende = generer_banditt(spiller)
            elif tall >= 4:
                fiende = generer_kvist(spiller)
            elif tall >= 2:
                fiende = generer_mosegrodd_stein(spiller)
            else:
                fiende = generer_liten_sopp(spiller)

            skogen = angrip(spiller, fiende, inv, klasser, spellbook)

        while sopp:
            if not bQlog.hent_quest(2).ferdig():
                print("\n    Sopp:" + Fore.RED  + """ Patetiske lille menneske, gjør som vi befaler!
          Du skal dra ut i skogen, finne et tre vi har vurdert verdig, og lage et
          totem til ære for oss! Det kan alle dere små skapninger bruke til å tilbe
          oss. Du vet at vi har vurdert et tre verdig hvis det angriper deg. Gi
          totemet til en av våre mest fanatiske tilhengere. Dra nå!

          Skulle du komme tilbake til dette hemmelige soppstedet senere, kan vi
          restorere deg til ditt fulle potensiale, men kun hvis du viser deg verdig
          vår velsignelse.\n""" + Style.RESET_ALL)
                sopp = False
                bQlog.hent_quest(2).progresser()
                input("Trykk enter for å fortsette\n> ")
            elif angrip(spiller, generer_liten_sopp(spiller), inv, klasser, spellbook):
                print("\n" + spiller.navn(), "fikk restorert", spiller.restorer(1000), "helsepoeng og", \
                spiller.restorer_kp(300), " konsentrasjonspoeng gjennom de magiske soppenes velsignelse.\n")
                input("Trykk enter for å fortsette\n> ")
            sopp = False

        while duell:
            progresjon = 6 + sum([int(bQlog.hent_quest(x).ferdig()) for x in range(6, len(bQlog.hent_qLog()))])
            try:
                q = bQlog.hent_quest(progresjon)
            except IndexError:
                print("\n        *Det er ingen flere å duellere mot her*\n")
                input("Trykk enter for å fortsette\n> ")
                duell = False
                break
            if progresjon != 11 or bQlog.hent_quest(4).startet():
                q.sett_tilgjengelig()
            else:
                print("\n      *Onde Olga godter seg med seiersinntekten du skaffet henne*")
                print("      *Det er ingen flere å duellere mot på dette tidspunktet*\n")
                input("Trykk enter for å dra tilbake\n> ")
                duell = False
                break
            if not q.startet():
                bQlog.snakk(progresjon, spiller, inv)

            if q.startet() and q.progresjon():
                bQlog.snakk(progresjon, spiller, inv)
                duell = False
                if progresjon +1 != len(bQlog.hent_qLog()) and (progresjon+1 != 11 or bQlog.hent_quest(4).startet()):
                    if input("\nVil du høre om neste duellant?\n> ").lower() in {"j", "ja", "yes", "y"}:
                        duell = True
                if bQlog.hent_quest(11).ferdig():
                    bQlog.hent_quest(4).progresser()

            elif q.startet() and inv.penger() >= 500:
                inv.penger(-500)
                print("Du blir trukket 500 gullstykker for inngangsbillett.")
                input("Trykk enter for å fortsette\n> ")
                fiende = generer_duellant(progresjon - 6)
                if angrip(spiller, fiende, inv, klasser, spellbook):
                    q.progresser()
                else:
                    duell = False

            elif q.startet():
                print("\nDu har ikke nok gullstykker til å bli med i en duell!\n")
                input("Trykk enter for å dra tilbake til leiren\n> ")
                duell = False

            else:
                duell = False

            q.sett_tilgjengelig(False)

    if ferdig:
        return False

def kjellLoop(spiller, inv, klasser, spellbook, kjellQ):
    q = klasser.questlog(6).hent_quest(2)
    if kjellQ.sjekk_ferdig():
        print("    Hvorfor er du fremdeles her og slenger? Se til å gi den forbaskede",\
        "\n    fingeren til den hersens banditten!")
        input("\nTrykk enter for å fortsette\n> ")
        return True
    elif q.sjekk_ferdig() and not q.ferdig():
        print("\n    Supert", spiller.navn() + "! Her har du en kopi av fingeren min!\n")
        q.reward(inv, spiller, klasser.questlog(6))
        q.sett_ferdig()
        kjellQ.progresser()
        input("Trykk enter for å fortsette\n> ")
        return True
    elif q.startet():
        print("""    Tresorten du leter etter heter Guffsliffsaff, og finnes
    rundt omkring her i skogen. Den er relativt sjelden, men du burde støte
    på den før eller siden. Kom tilbake hit når du har funnet den, og pass
    på å ikke være borti den selv!\n""")
        input("Trykk enter for å fortsette\n> ")
        return True
    print("\n    " + spiller.navn() + """!
    Hva sier du, vil du ha fingeren min? Det er den mest uforskammede
    forespørselen jeg noensinne har hørt! Om du vil ha den, må du sloss
    mot meg først! Ved mindre...

    Jeg har en idé. Om det er sant som du sier, at dette er den eneste
    måten å få de forbeskede bandittene til å slutte å jakte oss, burde
    jeg gi deg fingeren. Og jeg tror jeg har en måte vi kan gjøre det
    på uten å ta frem kniven.""")
    input("\nTrykk enter for å fortsette\n> ")
    print("""
    Gjennom århundrer med å nøye observere tresorter, har jeg funnet en
    bemerkelsesverdig tresort som har en helt spesiell egenskap; Dens
    grener kan etterligne det de kommer i kontakt med! Det eneste du
    trenger å gjøre er å finne tresorten, temme den og ta den med til
    meg. Den kan være noe aggressiv, så pass på!\n""")
    if input("Ønsker du å hjelpe Kjedelige Kjell å beholde fingeren sin?   (ja/nei)\n> ").lower() in {"ja", "j"}:
        q.start()
        print("""\n    Strålende! Tresorten du leter etter heter Guffsliffsaff, og finnes
    rundt omkring her i skogen. Den er relativt sjelden, men du burde støte
    på den før eller siden. Kom tilbake hit når du har funnet den, og pass
    på å ikke være borti den selv!\n""")
        input("Trykk enter for å fortsette\n> ")
        return True
    elif input("\nØnsker du å angripe Kjedelige Kjell og kutte av ham fingeren?\n> ").lower() in {"ja", "j"}:
        loot = Loot()
        loot.legg_til_item(400, 1)
        fiende = Fiende("Kjedelige Kjell", "magiker", loot, a=350, hp=3000, d=240, kp=350, bonusKp=4)
        if not angrip(spiller, fiende, inv, klasser, spellbook):
            return False
        kjellQ.progresser()
    return True

def ussleUlvLoop(spiller, inv, klasser, spellbook):
    print("    Tusen takk " + spiller.navn() + """!
    Nå kan jeg endelig vinne hjertet til Fagre Frida! Håper ikke jeg må
    sloss mot eksen hennes, har hørt hun er ganske grusom...

    Uansett, takk for hjelpen! Dessverre kan jeg ikke etterlate noen
    løse tråder, tenk om andre skulle lært de samme kunstene av deg?
    Da ville jeg ikke vært særlig spesiell lengre! Dette har vært gøy,
    men jeg er redd det er på tide for deg å opphøre å eksistere.\n""")
    input("Trykk enter for å fortsette\n> ")
    print("\nUssle Ulv har knivstukket deg!")
    skade = spiller.hp() // 3
    spiller.mist_liv(skade)
    print(spiller.navn(), "mistet", skade, "liv!\n")
    loot = Loot()
    loot.legg_til_item(30, 1)
    ussleUlv = Fiende("Ussle Ulf", "snik", loot, a=400, d=200, hp=3000, kp=500, weapon=200, bonusKp=8)
    if angrip(spiller, ussleUlv, inv, klasser, spellbook):
        klasser.questlog(7).hent_quest(1).progresser_liste(0)
        return True
    return False

def angrip(spiller, fiende, inv, klasser, spellbook):
    sQlog = klasser.questlog(6)
    bQlog = klasser.questlog(7)
    skriv_ut(spiller, fiende)
    uCD = 0
    bundetCD = 0
    while True:
        #tur angir at det er brukeren sin tur til å handle.
        if bundetCD > 0:
            tur = False
            inn = ""
            print(spiller.navn(), "er bundet fast.")
        else:
            inn = input("\nHva vil du gjøre?\n> ").lower()
            tur = kommandoer(inn, spiller, fiende, inv, klasser, spellbook)

        if inn == "f" or inn == "flykt":
            print(spiller.navn(), "drar tilbake til leiren.")
            return False

        #Her sjekkes om fienden er død. Om så, får karakteren loot og xp.
        if fiende.dead():
            print("--------------------------------------------------------------------"+\
            "\nDu vant!", fiende.navn() + fiende.ending(), "er overvunnet!",spiller.navn(),"får",fiende.xp(),"erfaringspoeng.")
            spiller.kons()
            spiller.gi_xp(fiende.xp())
            fiende.loot(spiller, inv)

            #Quests:
            #Banditt q1:
            if fiende.navn() == "Banditt" and bQlog.hent_quest(0).startet() and not \
            bQlog.hent_quest(0).ferdig() and randint(0, 2) == 1:
                print("Du fant et av Lugubre Lasses lommeur!")
                bQlog.hent_quest(0).progresser()

            #Banditt q6:
            if fiende.navn() == "Kjedelige Kjell":
                print("Du kutter av fingeren til Kjedelige Kjell")
                print("Du får 3 ondhetspoeng.")
                spiller.evil_points(3)

            #Shroom bq1
            if fiende.race() == "tre" and bQlog.hent_quest(2).ferdig() and not sQlog.hent_quest(1).ferdig()\
            and randint(1, 5) == 1:
                sQlog.hent_quest(1).progresser()
                print("Du klarte å lage et totem ut av restene til", fiende.navn() + fiende.ending())

            #Shroom q10
            if fiende.race() == "guffsliffsaff" and sQlog.hent_quest(2).startet() \
            and not sQlog.hent_quest(2).progresjon():
                sQlog.hent_quest(2).progresser()
                print("Du plukker opp de tamme restene av guffsliffsaff-grenen.")

            input("Trykk enter for å fortsette\n> ")
            return True

        elif not tur:
            #Guffsliffsaff - spiller til tre
            if fiende.navn() == spiller.navn() + " v2" and fiende.hp() <= int(fiende.xHp() / 4):
                print("Guffsliffsaffen er for svak til å opprettholde formen sin!")
                print("Guffsliffsaffen transformerer seg igjen.")
                fiende = generer_guffsliffsaff(spiller, "kvist", fiende)
                input("Trykk enter for å fortsette")
            #Utforsk
            elif fiende.race() == "snik" and fiende.kp() >= 195 and uCD >=0 and randint(1, 5) >= 3:
                print(fiende.navn() + fiende.ending(), "kastet Utforsk!")
                fiende.bruk_kons(195)
                uCD = -6
            #Smidige Sandra - Duell
            elif fiende.navn() == "Smidige Sandra":
                if fiende.untouchableCD():
                    print("Smidige Sandra restorerte 800 hp.")
                    fiende.restorer(800)
                    fiende.kp(-15)
                elif fiende.hp() < 900 and fiende.kp() >= 100 and not fiende.untouchableCD():
                    print("Smidige Sandra har sklidd inn i mørket for to runder!")
                    fiende.set_untouchable(True, 2)
                    fiende.kp(-100)
                elif fiende.kp() >= 150 and randint(1, 4) == 1 and bundetCD <= 0:
                    print("Smidige Sandra har bundet deg fast!")
                    bundetCD = 3
                    fiende.kp(-150)
                else:
                    spiller.angrepet(fiende)
            #Store Sture - Duell
            elif fiende.navn() == "Store Sture":
                if fiende.kp() >= 50 and fiende.hp() <= fiende.xHp() - 210 and randint(1, 5) == 3:
                    print("Store Sture dunket deg med et kjøttstykke og spiste det!")
                    print(fiende.navn(), "restorerte", fiende.restorer(250), "hp.")
                    print(spiller.navn(), "mistet", spiller.mist_liv(50), "liv.")
                    fiende.kp(-50)
                else:
                    spiller.angrepet(fiende)
            #Kraftige Klara - Duell
            elif fiende.navn() == "Kraftige Klara":
                if fiende.kp() >= 50 and randint(1, 7) != 1:
                    fiende.kp(-50)
                    fiende.a(500)
                    print("Kraftige Klara varmet opp musklene!")
                    print("Kraftige Klara fikk 500 angrepspoeng.")
                else:
                    spiller.angrepet(fiende)
            #Teite Tim - Duell
            elif fiende.navn() == "Teite Tim":
                if fiende.kp() >= 200 and randint(1, 15) == 7 and fiende.hp() < fiende.xHp() - 400:
                    print("Teite Tim kastet Super Restituer!")
                    print("Teite Tim restorerte", fiende.restorer(500 + randint(0, 120)), "liv.")
                    fiende.kp(-200)
                elif fiende.kp() >= 350 and randint(1, 10) == 1 and spiller.kp() >= 150:
                    print("Teite Tim kastet Distraher!")
                    print(spiller.navn(), "mistet", spiller.mist_kp(500 + randint(0, 80)), "kp.")
                    fiende.kp(-350)
                elif fiende.kp() >= 200 and randint(1, 15) == 1:
                    print("Teite Tim gjorde en strategisk vurdering av kampen!")
                    print("Teite TIm fikk 50 angrepspoeng.")
                    fiende.a(50)
                    fiende.kp(-200)
                elif fiende.kp() >= 50 and randint(1, 8) == 1 and uCD >= 0:
                    print("Teite Tim kastet Restituer!")
                    print("Teite Tim restorerte", fiende.restorer(150 + randint(0, 50)), "liv.")
                    fiende.kp(-50)
                else:
                    if uCD < 0:
                        print(fiende.navn() + fiende.ending(), "restorerte", fiende.restorer(spiller.angrepet(fiende)), "hp!")
                    else:
                        spiller.angrepet(fiende)
            #Onde Olga - Duell
            elif fiende.navn() == "Onde Olga":
                if fiende.kp() >= 315 and randint(1, 7) == 1 and not fiende.untouchableCD():
                    print(fiende.navn() + fiende.ending(), "kastet RockNoRoll!")
                    print(fiende.navn() + fiende.ending(), "er blitt til stein!")
                    fiende.kp(-315)
                    fiende.set_untouchable(True, 5)
                elif fiende.kp() >= 140 and randint(1, 6) == 1 and fiende.hp() < fiende.xHp() - 200:
                    print("Onde Olga kastet Restituer!")
                    print("Onde Olga restorerte", fiende.restorer(250), "liv.")
                    fiende.kp(-140)
                elif fiende.kp() >= 350 and randint(1, 2 + round(13 * (fiende.hp() / fiende.xHp()))) == 1:
                    print("Onde Olga mante frem en kampstein og kastet den på deg!")
                    print(spiller.navn(), "mistet", spiller.mist_liv(500), "liv!")
                    fiende.kp(-350)
                else:
                    spiller.angrepet(fiende)
            #Restituer
            elif fiende.kp() >= 50 and randint(0, 2) == 1 and fiende.hp() < (fiende.xHp() - 90) and uCD >= 0:
                print(fiende.navn() + fiende.ending(), "kastet Restituer!")
                print(fiende.navn() + fiende.ending(), "restorerte", fiende.restorer(100), "hp.")
                fiende.bruk_kons(50)
            #Guffsliffsaff
            elif fiende.navn() == "Guffsliffsaff" and fiende.kp() >= 60 and randint(1, 3) == 1:
                print(fiende.navn() + fiende.ending(), "tok på deg!")
                print(fiende.navn() + fiende.ending(), "transformerer seg.")
                input("Trykk enter for å fortsette\n> ")
                fiende = generer_guffsliffsaff(spiller, True)
            #Vanlig angrep
            else:
                if uCD < 0:
                    print(fiende.navn() + fiende.ending(), "restorerte", fiende.restorer(spiller.angrepet(fiende)), "hp!")
                else:
                    spiller.angrepet(fiende)

            #gir beskjed om karakteren døde
            if spiller.dead():
                write_player_died(spiller, "leiren")
                player_died(spiller, inv, klasser)
                return False

            #skriver ut hp og kp til karakteren og hp til fienden til neste runde.
            else:
                uCD += 1
                bundetCD -= 1
                spiller.kons()
                fiende.gen_kons()
                skriv_ut(spiller, fiende)
                if bundetCD > 0:
                    input("Trykk enter for å fortsette\n> ")

def generer_mosegrodd_stein(spiller):
    loot = Loot()
    loot.legg_til_item(100, 1)
    return Fiende("Mosegrodd stein", "stein", loot,  a=100, d=100, hp=100, kp=100)

def generer_kvist(spiller):
    loot = Loot()
    a = randint(0, 4 * spiller.lvl())
    xKp = randint(0, 3 * spiller.lvl())
    item = Item("Superkvist", "weapon", a=a, xKp=xKp)
    loot.legg_til_item(item, 100)
    fiende = Fiende(navn="Kvist", race="tre", loot=loot, \
    hp=20 + 20 * randint(1, spiller.lvl()), \
    a=20 + randint(0, 10 * spiller.lvl()), \
    d=30 + randint(0, 10 * spiller.lvl()), \
    kp=50 + randint(0, 3 * spiller.lvl()), bonusKp=2, ending="en")
    print("\n" + spiller.navn(), "har møtt på en levende kvist!")

    #skrivKvist()
    return fiende

def generer_tre(spiller):
    pass

def generer_guffsliffsaff(spiller, b=False, fSpiller=None):
    loot = Loot()
    loot.legg_til_item(75, 1)
    if not b:
        return Fiende("Guffsliffsaff", "guffsliffsaff", loot, a=200, hp=2300, d=200, kp=200, bonusKp=7, ending="en")
    elif b is "kvist":
        fiende = Fiende("Guffsliffsaff-gren", "guffsliffsaff", loot, a=200, hp=2300, d=200, kp=200, bonusKp=7, ending="en")
        fiende.mist_liv(2300 - round((fSpiller.hp() / fSpiller.xHp()) *2300), stille=True)
        return fiende
    return Fiende(spiller.navn() + " v2", "guffsliffsaff", loot, a=spiller.a(), hp=spiller.xHp(),\
    d=spiller.d(), kp=spiller.xKp(), bonusKp=spiller.ekstraKp()-5)

def generer_duellant(nr):
    fiende = None
    loot = Loot()
    if nr == 0:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Patetiske Patrick", "menneske", loot, a=300, hp=850, d=200)
    elif nr == 1:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Store Sture", "menneske", loot, a=200, hp=10000, d=200, kp=200, bonusKp=1)
    elif nr == 2:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Smidige Sandra", "menneske", loot, a=300, hp=2300, d=400, kp=450, bonusKp=10)
    elif nr == 3:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Kraftige Klara", "menneske", loot, a=1200, hp=1337, d=-1200, kp=50)
    elif nr == 4:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Teite Tim", "snik", loot, a=400, hp=6666, d=1000, kp=600, bonusKp=8)
    elif nr == 5:
        loot.legg_til_item(50, 1)
        fiende = Fiende("Onde Olga", "gargyl", loot, a=1000, hp=5734, d=666, kp=1000, bonusKp=20, weapon=250)
    return fiende

def generer_banditt(spiller):
    loot = Loot()
    fiende = Fiende("Banditt", "menneske", loot, hp=1400, a=250, d=170, ending="en")
    bandittLoot(loot, fiende, spiller)
    skrivBanditt()
    print("\n" + spiller.navn(), "har møtt på en banditt!")
    return fiende

def generer_liten_sopp(spiller):
    loot = Loot()
    loot.legg_til_item(100, 1)
    return Fiende("Liten sopp", "shroom", loot, a=100, d=100, hp=100, kp=100)

def bandittLoot(loot, fiende, spiller):
    loot.legg_til_item(100, 60)

    kpkp = int(randint(1, spiller.lvl()) /10) *25 + 100
    item = Item("Konsentrasjonspulver", "restoring", kp=kpkp)
    item.sett_loot_tekst("en stripe konsentrasjonspulver")
    loot.legg_til_item(item, 8)

    a = randint(40, 40 + 5 * spiller.lvl())
    item = Item("Sverd", "weapon", a=a, blade=True)
    item.sett_loot_tekst("et sverd")
    loot.legg_til_item(item, 5)

def dynamiskLoot(loot, fiende, spiller):
    tall = round(10 + fiende.xp() / 10)
    loot.legg_til_item(tall, 60)

    item = Item("Tryllepulver", "damaging", dmg=100)
    item.sett_loot_tekst("en håndfull tryllepulver")
    loot.legg_til_item(item, 17)

    kpkp = int(randint(1, spiller.lvl()) /10) *25 + 100
    item = Item("Konsentrasjonspulver", "restoring", kp=kpkp)
    item.sett_loot_tekst("en stripe konsentrasjonspulver")
    loot.legg_til_item(item, 8)

    tdhp = randint(1, spiller.lvl()) * 5 + 145
    item = Item("Trolldrikk", "restoring", hp=tdhp)
    loot.legg_til_item(item, 13)

    a = randint(0, 4 * spiller.lvl())
    xKp = randint(0, 3 * spiller.lvl())
    item = Item("Tryllestav", "weapon", a=a, xKp=xKp)
    loot.legg_til_item(item, 5)

    a = randint(40, 40 + 5 * spiller.lvl())
    item = Item("Sverd", "weapon", a=a, blade=True)
    item.sett_loot_tekst("et sverd")
    loot.legg_til_item(item, 5)

    xHp = randint(0, 4 * spiller.lvl())
    d = randint(0, 2 * spiller.lvl())
    item = Item("Spiss Hatt", "hat", xHp=xHp, d=d)
    loot.legg_til_item(item, 5)

def skog_kart(qlog):
    print("""
    Velkommen til ekspedisjonsleiren! Her er stedene du kan dra:
    Skogen (s)                 Utforsk området utenfor ekspedisjonsleiren
    Butikken (k)               Se gjennom nødrasjonene og spesial-utstyret
    Strategi-teltet (q)        Diskuter strategi med de andre i ekspedisjonen
    Leirbålet (b)              Dra tilbake til det forlatte leirbålet
    Minnesteinen (l)           Graver din progresjon i skogens omtrent-funksjonelle minnestein""")
    print("    Ut i verden (f)            Viser deg kart over alle stedene du kan dra\n")

def banditt_kart(qlog):
    print("""
    Velkommen til banditt-leiren! Her er stedene du kan dra:
    Skogen (s)                 Se hvem du finner i utkanten av leiren
    Stortreet (q)              Dra til det største treet og hør bandittenes forpinte bønner om hjelp
    Svartemarkedet (k)         Få en god pris på Gundis utvalgte favorittbytter
    Duellringen (d)            Test dine ferdigheter i bandittenes interne duellring""")
    if qlog.hent_qLog()[2].startet():
        print("    Soppstedet (p)             Dra til det hemmelige soppstedet")
    print("    Ekspedisjonsleiren (f)     Dra tilbake til ekspedisjonsleiren\n")

def shroom_butikk(butikk):
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

    item = Item("Sverd", "weapon", a=100, xHp=20)
    vare = Vare(item, 3000, "v")
    butikk.legg_til_vare(vare)

    item = Item("falskt skjegg", "beard", xKp=30, ekstraKp=3)
    vare = Vare(item, 1100, "g")
    butikk.legg_til_vare(vare)

def banditt_butikk(butikk):
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

    item = Item("Sverd", "weapon", a=100, xHp=20)
    vare = Vare(item, 3000, "v")
    butikk.legg_til_vare(vare)

    item = Item("falskt skjegg", "beard", xKp=30, ekstraKp=3)
    vare = Vare(item, 1100, "g")
    butikk.legg_til_vare(vare)

def skog_quest(qlog, spiller):
    navn = spiller.navn()

    #q1
    desk1 = shroom_q1(navn)
    ferdigDesk1 = shroom_q1_ferdig(navn)
    q1 = Quest(desk1, ferdigDesk1, 1, 15, "Zip")
    q1.legg_til_reward(xp=10000, gull=300, hp=30, kp=30)
    q1.legg_til_progresjonTekst("Banditt-angrep stoppet: ")
    q1.legg_til_svarTekst("\nVil du gå på bandittjakt?     (ja/nei)\n> ")
    qlog.legg_til_quest(q1)

    #bq1
    deskBq1 = shroom_bq1(navn)
    ferdigDeskBq1 = shroom_bq1_ferdig(navn)
    bq1 = Quest(deskBq1, ferdigDeskBq1, 1, 1, "Fanatiske Ferdinand", bonus=True, resetIfDead=True)
    item = Item("Forkastet totem", "trinket", xKp=50, xHp=60, ekstraKp=3, d=20)
    bq1.legg_til_reward(xp=6000, item=item, gp=2)
    bq1.legg_til_progresjonTekst("Totem funnet: ")
    bq1.legg_til_svarTekst("Vil du fortelle Fanatiske Ferdinand at han er hjernevasket?   (ja/nei)\n> ")
    bq1.legg_til_ekstra_tekst("Hvaaaa? Det kan umulig stemme? De- dette, men, hvorfor? Hvem er jeg? HVEM ER JEG??")
    bq1.legg_til_alt_desk("Vil du gi totemet til Fanatiske Ferdinand?\n> ")
    item = Item("Fanatisk stav", "weapon", a=200, d=-10, xHp=-30)
    bq1.legg_til_alt_reward(ep=3, kp=50, xp=6000, item=item)
    qlog.legg_til_quest(bq1)

    #q10
    q10 = Quest("", "", 1, 15, "Kjedelige Kjell", tilgjengelig=False, resetIfDead=True)
    q10.legg_til_reward(xp=1000, gp=2)
    q10.legg_til_progresjonTekst("Guffsliffsaff-gren funnet: ")
    qlog.legg_til_quest(q10)

def banditt_quest(qlog, spiller):
    navn = spiller.navn()

    #q1
    desk1 = banditt_q1(navn)
    ferdigDesk1 = banditt_q1_ferdig(navn)
    q1 = Quest(desk1, ferdigDesk1, 4, 20, "Lugubre Lasse", resetIfDead=True)
    q1.legg_til_reward(xp=3000, gull=1000, hp=30, kp=30)
    q1.legg_til_progresjonTekst("Lommeur funnet: ")
    q1.legg_til_svarTekst("\nKan du hjelpe meg å stjele tilbake lommeurene mine?     (ja/nei)\n> ")
    qlog.legg_til_quest(q1)

    #q2
    desk2 = banditt_q2(navn)
    ferdigDesk2 = banditt_q2_ferdig(navn)
    q2 = Quest(desk2, ferdigDesk2, 6, 22, "Ussle Ulf")
    item = Item("Usselt sverd", "weapon", blade=True, a=200, xHp=-150, ekstraKp=-2)
    q2.legg_til_reward(xp=5000, gull=600, item=item, settTilgjengelig=True, settTilgjengeligIndeks=4)
    q2.legg_til_progresjonTekst("Utforsk kastet: ")
    q2.legg_til_progresjon(1)
    q2.legg_til_progresjonTekstListe("Ussle Ulf undervist: ", 0)
    q2.legg_til_svarTekst("\nKan du lære meg hvordan få bedre helse ved å utforske innmaten til fienden?     (ja/nei)\n> ")
    qlog.legg_til_quest(q2)

    #q3
    desk3 = banditt_q3(navn)
    ferdigDesk3 = banditt_q3_ferdig(navn)
    q3 = Quest(desk3, ferdigDesk3, 1, 23, "Godtroende Gudleif")
    q3.legg_til_reward(xp=3000, kp=10)
    q3.legg_til_progresjonTekst("Soppsted besøkt: ")
    q3.legg_til_svarTekst("\nEr du klar for å åpne sinnet ditt mot høyere makter?     (ja/nei)\n> ")
    qlog.legg_til_quest(q3)

    #q4
    desk4 = banditt_q4(navn)
    ferdigDesk4 = banditt_q4_ferdig(navn)
    q4 = Quest(desk4, ferdigDesk4, 8, 25, "Taktiske Tore")
    q4.legg_til_reward(xp=3000, kp=10)
    q4.legg_til_progresjonTekst("Fiender distrahert: ")
    q4.legg_til_svarTekst("\nVil du trene deg opp til å bli en mester-banditt?     (ja/nei)\n> ")
    qlog.legg_til_quest(q4)

    #q5
    desk5 = banditt_q5(navn)
    ferdigDesk5 = banditt_q5_ferdig(navn)
    q5 = Quest(desk5, ferdigDesk5, 1, 26, "Fagre Frida", tilgjengelig=False)
    q5.legg_til_reward(xp=3000, kp=10)
    q5.legg_til_progresjonTekst("Onde Olga bekjempet: ")
    q5.legg_til_svarTekst("\nVil du, min helt, utfordre eksen min til duell?     (ja/nei)\n> ")
    qlog.legg_til_quest(q5)

    #q6
    desk6 = banditt_q6(navn)
    ferdigDesk6 = banditt_q6_ferdig(navn)
    q6 = Quest(desk6, ferdigDesk6, 1, 28, "Bjarte Banditt")
    q6.legg_til_reward(xp=10000, gull=300, hp=30, kp=30)
    q6.legg_til_progresjonTekst("Kjedelige Kjells finger kuttet: ")
    q6.legg_til_svarTekst("\nVil du 'ordne' Kjedelige Kjell?     (ja/nei)\n> ")
    qlog.legg_til_quest(q6)

    #duell_q1
    desk = banditt_dq7(navn)
    ferdigDesk = banditt_dq7_ferdig(navn)
    dq7 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq7.legg_til_reward(xp=2000, gull=1000)
    dq7.legg_til_progresjonTekst("Patetiske Patrick overvunnet: ")
    dq7.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq7)

    #duell_q2
    desk = banditt_dq8(navn)
    ferdigDesk = banditt_dq8_ferdig(navn)
    dq8 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq8.legg_til_reward(xp=3000, gull=1500, hp=150, d=40)
    dq8.legg_til_progresjonTekst("Store Sture overvunnet: ")
    dq8.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq8)

    #duell_q3
    desk = banditt_dq9(navn)
    ferdigDesk = banditt_dq9_ferdig(navn)
    dq9 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq9.legg_til_reward(xp=5000, gull=2000, kp=50)
    dq9.legg_til_progresjonTekst("Smidige Sandra overvunnet: ")
    dq9.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq9)

    #duell_q4
    desk = banditt_dq10(navn)
    ferdigDesk = banditt_dq10_ferdig(navn)
    dq10 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq10.legg_til_reward(xp=8000, gull=3000, a=50, kp=10)
    dq10.legg_til_progresjonTekst("Kraftige Klara overvunnet: ")
    dq10.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq10)

    #duell_q5
    desk = banditt_dq11(navn)
    ferdigDesk = banditt_dq11_ferdig(navn)
    dq11 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq11.legg_til_reward(xp=12000, gull=5000, hp=10, kp=10, ekstraKp=2)
    dq11.legg_til_progresjonTekst("Teite Tim overvunnet: ")
    dq11.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq11)

    #duell_q6
    desk = banditt_dq12(navn)
    ferdigDesk = banditt_dq12_ferdig(navn)
    dq12 = Quest(desk, ferdigDesk, 1, 1, "Onde Olga", tilgjengelig=False)
    dq12.legg_til_reward(xp=20000, gull=7000, hp=50, kp=40, d=15, a=15, ekstraKp=1)
    dq12.legg_til_progresjonTekst("Onde Olga overvunnet: ")
    dq12.legg_til_svarTekst("\nEr du klar for duellringen?     (ja/nei)\n> ")
    qlog.legg_til_quest(dq12)
