# larp-ilmo

## Web-sovellus liveroolipelien ilmoittautumislomakkeiden luomiseen ja täyttämiseen

Sovellus tarjoaa liveroolipelien järjestäjille mahdollisuuden rekisteröityä palveluun pelinjärjestäjiksi ja luoda peliään varten mukautettu ilmoittautumislomake käyttäen hyväksi sekä valmiiksi luotuja vakiokysymyksiä että valmiiksi määriteltyjen kenttätyyppien (esim. vapaa tekstivastaus, monivalinta, samaa mieltä / eri mieltä -asteikko) pohjalta itse luomiaan kysymyksiä ja julkaista lomake täytettäväksi. Muut käyttäjät voivat täyttää ilmoittautumislomakkeen ja tallentaa sen tietokantaan, jossa kyseisen pelin järjestäjä voi tarkastella täytettyjä ilmoittautumisia.

## Sovelluksen toiminnallisuudet

Merkityt (&#x2713;) kohdat on jo toteutettu sovelluksen tämänhetkisessä versiossa; loput tullaan toteuttamaan projektin toisessa vaiheessa. Myös sovelluksen käyttämä tietokantarakenne on kokonaisuudessaan toteutettu, joskin siihen saattaa vielä tulla pieniä muutoksia projektin toisessa vaiheessa. Sovelluksen ulkoasulle ei ole vielä tehty minkäänlaista kehitystyötä, joten se on kauniisti sanoen alkeellinen, mutta sen ei pitäisi juurikaan haitata sovelluksen käyttöä.

### Pelinjärjestäjälle

- tunnuksen luonti &#x2713;
- pelin tietojen syöttäminen &#x2713;
- ilmoittautumislomakkeen luonti &#x2713;
- kysymysten lisääminen lomakkeeseen &#x2713; (osittain)
- uusien kysymysten luonti (kenttätyyppi + vastausvaihtoehdot) &#x2713; (osittain)
- lomakkeen julkaiseminen &#x2713;
- täytettyjen lomakkeiden vastausten tarkastelu &#x2713;
- pelin ilmoittautumisten tallennus json-tiedostona

### Käyttäjälle
- tunnuksen luonti &#x2713;
- palvelussa julkaistujen pelien tarkastelu &#x2713;
- ilmoittautumislomakkeen täyttäminen &#x2713; 
- omien tietojen täyttäminen automaattisesti käyttäjäprofiilista &#x2713;
- ilmoittautumislomakkeen lähettäminen &#x2713;

## Tarvittavat sivut / näkymät
- sisäänkirjaus &#x2713;
- rekisteröityminen &#x2713;
- omien tietojen muokkaus &#x2713;
- pelin luonti &#x2713;
- pelin tietojen muokkaaminen &#x2713;
- ilmoittautumislomakkeen luonti &#x2713;
- uuden kysymyksen luonti &#x2713; (osittain)
- julkaistut pelit &#x2713;
- ilmoittautumislomakkeen täyttö &#x2713;
- ilmoittautumisluettelo &#x2713;
- yksittäisen ilmoittautumisen tarkastelu &#x2713;

## Sovelluksen tietokantarakenne
![Database diagram](https://github.com/vmarttil/larp-ilmo/blob/main/images/larp-ilmo_2.png)

## Sovelluksen käyttöhje (testausversio)

Sovellus on testattavissa osoitteessa [https://larp-ilmo.herokuapp.com/](https://larp-ilmo.herokuapp.com/).

### Pääsivu

Sovelluksen pääsivulla näkyy lista sovelluksessa julkaistuista peleistä ja niiden tietoja on mahdollista
tarkastella (myös kirjautumatta sovellukseen) klikkaamalla pelin nimeä listassa. Sivun yläreunassa on linkit 
sovellukseen rekisteröitymistä ja rekisteröityneiden käyttäjien sisäänkirjautumista varten. Rekisteröitymällä
on mahdollista luoda omia pelejä ja ilmoittautua muiden luomiin peleihin. Rekisteröityneet käyttäjät voivat 
muokata profiiliaan ja tarkastella omia ilmoittautumisiaan napsauttamalla omaa nimeään yläpalkissa.

### Pelin luonti

Sivun yläreunassa näkyy sisäänkirjautuneille käyttäjille linkki "Ilmoita peli", jonka kautta on mahdollista lisätä
sovellukseen uusi peli tietoineen ja luoda sille ilmoittautumislomake. Uuden pelin luonti -sivulla "Tallenna peli" 
tallentaa pelin tiedot, mutta ei vielä luo sille ilmoittautumislomaketta. Pelin luonut käyttäjä pääsee myöhemmin 
muokkaamaan pelin tietoja pääsivun peliluettelossa näkyvän "Muokkaa"-linkin kautta, ja tätä kautta voi myös luoda 
pelille ilmoittautumislomakkeen. 

### Ilmoittautumislomakkeen luonti

Pelin luonti- ja muokkausivun painike "Luo ilmoittautumislomake" luo pelille ilmoittautumislomakkeen ja avaa sen
näkyviin. Aluksi lomakkeessa on oletuskysymykset, ja tällä hetkellä käyttäjä voi vaihdella niiden järjestystä ja 
lisätä lomakkeeseen uusia tekstikenttä, numerokenttä ja tekstialue-tyyppisiä kysymyksiä. Kysymysten muokkaamista 
ja poistamista eikä valintoja sisältävien kysymysten ja niiden valintojen lisäämistä ei ole vielä toteutettu; 
lopullisessa versiossa käyttäjä voi poistaa kysymyksiä, muokata niitä ja luoda myös valintatyyppisiä kysymyksiä. 
Ilmoittautumislomakkeen muokkausnäkymän alareunassa on "Avaa ilmoittautuminen" -painike, joka julkaisee 
ilmoittautumislomakkeen siten, että kaikki sisään kirjautuneet käyttäjät pystyvät ilmoittautumaan 
peliin pääsivun listassa näkyvän "Ilmoittaudu"-linkin kautta. Kun ilmoittautuminen on avattu, "Avaa ilmoittautuminen" 
-painike korvautuu "Sulje ilmoittautuminen" -painikkeella, joka poistaa ilmoittautumislinkin pääsivun listasta ja 
estää uusien ilmoittautumisten tekemisen. Muokkausnäkymän alareunassa on myös painike, jolla lomaketta voi esikatsella 
siinä muodossa kun se tulee näkymään käyttäjälle, mutta ilman täyttömahdollisuuta.

### Ilmoittautuminen

Kun pelin luonut käyttäjä on avannut pelin ilmoittautumisen, kuka tahansa kirjautunut käyttäjä voi ilmoittautua peliin 
klikkaamalla etusivun listassa olevaa "Ilmoittaudu" -linkkiä ja täyttämällä avautuvan ilmoittautumislomakkeen. Kun lomake 
on täytetty ja käyttäjä klikkaa sivun alareunassa olevaa "Ilmoittaudu"-painiketta, ilmoittautumisen tiedot tallennetaan 
tietokantaan ja sovellus palauttaa käyttäjän pääsivulle. Käyttäjä voi tarkastella omia ilmoittautumisiaan omalla profiilisivulla
ja pelin luonut käyttäjä näkee pelin tietojen alla siihen tehdyt ilmoittautumiset.


