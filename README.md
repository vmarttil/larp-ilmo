# larp-ilmo

## Web-sovellus liveroolipelien ilmoittautumislomakkeiden luomiseen ja täyttämiseen

Sovellus tarjoaa liveroolipelien järjestäjille mahdollisuuden luoda peliään varten mukautettu ilmoittautumislomake käyttäen hyväksi sekä valmiiksi luotuja vakiokysymyksiä että valmiiksi määriteltyjen kenttätyyppien (esim. lyhyt tekstikenttä, vapaa tekstivastaus, monivalinta) pohjalta itse luomiaan kysymyksiä ja julkaista lomake täytettäväksi. Muut käyttäjät voivat täyttää ilmoittautumislomakkeen ja tallentaa sen tietokantaan, jossa kyseisen pelin järjestäjä voi tarkastella täytettyjä ilmoittautumisia.

## Sovelluksen toiminnallisuudet

Sovellus sisältää tietokantarakenteet, palvelintoiminnallisuuden ja käyttöliittymän seuraaville toiminnallisuuksille:

### Pelinjärjestäjälle

- tunnuksen luonti
- pelin tietojen syöttäminen ja muokkaaminen
- ilmoittautumislomakkeen luonti
- kysymysten järjestäminen
- kysymysten muokkaaminen (kysymysteksti, tarkentava kuvaus ja valittavissa olevat vaihtoehdot)
- uusien kysymysten luonti ja lisääminen lomakkeeseen 
- ilmoittautumisen avaaminen ja sulkeminen
- täytettyjen lomakkeiden vastausten tarkastelu
- pelin ilmoittautumisten tallennus json-tiedostona

### Käyttäjälle
- tunnuksen luonti
- oman profiilin tarkastelu ja muokkaus
- palvelussa julkaistujen pelien ja niiden tietojen tarkastelu
- ilmoittautumislomakkeen täyttäminen
- omien tietojen täyttäminen ilmoittautumislomakkeeseen automaattisesti käyttäjäprofiilista
- ilmoittautumislomakkeen lähettäminen
- omien ilmoittautumisten tarkastelu

## Sivut / näkymät
- sisäänkirjaus
- rekisteröityminen
- omien tietojen muokkaus
- pelin luonti
- pelin tietojen muokkaaminen
- ilmoittautumislomakkeen luonti
- ilmoittautumislomakkeen esitarkastelu
- uuden kysymyksen luonti 
- julkaistut pelit
- ilmoittautumislomakkeen täyttö
- ilmoittautumisluettelo
- yksittäisen ilmoittautumisen tarkastelu

## Sovelluksen tietokantarakenne
![Database diagram](https://github.com/vmarttil/larp-ilmo/blob/main/images/larp-ilmo_3.png)

## Sovelluksen käyttöhje

Sovellus on käytettävissä osoitteessa [https://larp-ilmo.herokuapp.com/](https://larp-ilmo.herokuapp.com/).

### Pääsivu

Sovelluksen pääsivulla näkyy lista sovelluksessa julkaistuista peleistä ja niiden tietoja on mahdollista
tarkastella (myös kirjautumatta sovellukseen) napsauttamalla pelin nimeä listassa. Sivun yläreunassa on linkit 
sovellukseen rekisteröitymistä ja rekisteröityneiden käyttäjien sisäänkirjautumista varten. Rekisteröitymällä 
on mahdollista luoda omia pelejä ja ilmoittautua muiden luomiin peleihin. Rekisteröityneet käyttäjät voivat 
muokata profiiliaan ja tarkastella omia ilmoittautumisiaan napsauttamalla omaa nimeään yläpalkissa.

### Pelien tarkastelu

Pelin nimeä pääsivun listassa napsauttamalla aukeaa pelin tietosivu, joka sisältää tiedot pelistä. Jos pelin 
ilmoittautuminen on avattu, pelin nimen perässä näkyy myös "Ilmoittaudu"-painike, josta pääsee täyttämään 
ilmoittautumislomaketta. Pelin järjestäjälle sivulla näkyy myös "Muokkaa"-painike sekä lista peliin tehdyistä 
ilmoittautumisista, joita voi tarkastella yksitellen napsauttamalla ilmoittautujan nimeä ja jotka voi ladata 
json-tiedostona napsauttamalla "Lataa ilmoittautumiset" -painiketta.

### Pelin luonti

Sivun yläreunassa näkyy sisäänkirjautuneille käyttäjille linkki "Ilmoita peli", jonka kautta on mahdollista lisätä
sovellukseen uusi peli tietoineen ja luoda sille ilmoittautumislomake. Uuden pelin luonti -sivulla "Tallenna peli" 
tallentaa pelin tiedot, mutta ei vielä luo sille ilmoittautumislomaketta. Pelin luonut käyttäjä pääsee myöhemmin 
muokkaamaan pelin tietoja joko pääsivun peliluettelossa näkyvän "Muokkaa"-linkin tai pelin tietosivulla olevan 
Muokkaa-painikkeen kautta, ja tätä kautta voi myös luoda pelille ilmoittautumislomakkeen. Pelin muokkausnäkymän 
alareunassa on myös "Avaa ilmoittautuminen" -painike, joka julkaisee ilmoittautumislomakkeen siten, että kaikki 
sisään kirjautuneet käyttäjät pystyvät ilmoittautumaan peliin pääsivun listassa ja pelin tietosivulla näkyvän 
"Ilmoittaudu"-linkin kautta. Kun ilmoittautuminen on avattu, "Avaa ilmoittautuminen" -painike korvautuu "Sulje 
ilmoittautuminen" -painikkeella, joka poistaa ilmoittautumislinkin pääsivun listasta ja estää uusien ilmoittautumisten 
tekemisen.

### Ilmoittautumislomakkeen luonti

Pelin luonti- ja muokkausivun painike "Luo ilmoittautumislomake" luo pelille ilmoittautumislomakkeen ja avaa sen
näkyviin. Aluksi lomakkeessa on oletuskysymykset, joista kaksi ensimmäistä ovat pakollisia. Käyttäjä voi vaihdella 
kysymysten järjestystä ja poistaa tai muokata niitä kysymyslaatikon oikeassa yläreunassa olevilla painikkeilla sekä
lisätä lomakkeeseen uusia tekstikenttä-, numerokenttä- ja tekstialue-tyyppisiä kysymyksiä. Kysymyksen poistopainike 
tuo näkyviin varmistusikkunan, jossa kysymyksen poiston voi varmistaa, ja kysymyksen muokkauspainike tuo näkyviin 
muokkausikkunan, jossa kysymyksen tietoja (kysymysteksti, kuvaus ja mahdolliset valinnat) voi muuttaa. Kysymyksen 
muokatut tiedot tallennetaan tietokantaan kun käyttäjä napsauttaa "Tallenna kysymys" -painiketta. Kysymyksiä voi lisätä 
lomakkeeseen valitsemalla lomakkeen alareunan "Lisää uusi kysymys" -kohdassa halutun kysymystyypin ja napsauttamalla 
"Lisää"-painiketta, jolloin aukeaa tyhjä kysymyksen muokkausikkuna. Muokkausnäkymän alareunassa on myös painike, jolla 
lomaketta voi esikatsella siinä muodossa kun se tulee näkymään käyttäjälle, mutta ilman täyttömahdollisuuta.

### Ilmoittautuminen

Kun pelin luonut käyttäjä on avannut pelin ilmoittautumisen, kuka tahansa kirjautunut käyttäjä voi ilmoittautua peliin 
napsauttamalla etusivun listassa olevaa "Ilmoittaudu" -linkkiä ja täyttämällä avautuvan ilmoittautumislomakkeen. Kun lomake 
on täytetty ja käyttäjä napsauttaa sivun alareunassa olevaa "Ilmoittaudu"-painiketta, ilmoittautumisen tiedot tallennetaan 
tietokantaan ja sovellus palauttaa käyttäjän pääsivulle. Käyttäjä voi tarkastella omia ilmoittautumisiaan omalla profiilisivulla
ja pelin luonut käyttäjä näkee pelin tietojen alla siihen tehdyt ilmoittautumiset.

## Mahdollisia lisätoiminnallisuuksia ja jatkokehitysideoita

- linkki pelin kotisivuille pelin tietoihin
- useamman tyyppisiä kysymyksiä (samaa/eri mieltä -asteikko, yms.)
- valintojen minimi- ja maksimimäärän määritys ilmoittautumislomakkeen valintaruutu-tyyppisille kysymyksille
- mahdollisuus lisätä omaan profiiliin tekstialue-kenttiä ja tuoda niiden sisältö ilmoittautumislomakkeen tekstialuekenttään
- pelin tiedot syöttäneelle käyttäjälle mahdollisuus lisätä muita käyttäjiä pelin järjestäjiksi