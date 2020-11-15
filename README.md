# larp-ilmo

## Web-sovellus liveroolipelien ilmoittautumislomakkeiden luomiseen ja täyttämiseen

Sovellus tarjoaa liveroolipelien järjestäjille mahdollisuuden rekisteröityä palveluun pelinjärjestäjiksi ja luoda peliään varten mukautettu ilmoittautumislomake käyttäen hyväksi sekä valmiiksi luotuja vakiokysymyksiä että valmiiksi määriteltyjen kenttätyyppien (esim. vapaa tekstivastaus, monivalinta, samaa mieltä / eri mieltä -asteikko) pohjalta itse luomiaan kysymyksiä ja julkaista lomake täytettäväksi. Muut käyttäjät voivat täyttää ilmoittautumislomakkeen ja tallentaa sen tietokantaan, jossa kyseisen pelin järjestäjä voi tarkastella täytettyjä ilmoittautumisia.

## Sovelluksen toiminnallisuudet

Merkityt (&#x2713;) kohdat on jo toteutettu sovelluksen tämänhetkisessä versiossa; loput tullaan toteuttamaan projektin toisessa vaiheessa. Myös sovelluksen käyttämä tietokantarakenne on kokonaisuudessaan toteutettu, joskin siihen saattaa vielä tulla pieniä muutoksia projektin toisessa vaiheessa. Sovelluksen ulkoasulle ei ole vielä tehty minkäänlaista kehitystyötä, joten se on kauniisti sanoen alkeellinen, mutta sen ei pitäisi juurikaan haitata sovelluksen käyttöä.

### Pelinjärjestäjälle

- tunnuksen luonti &#x2713;
- rekisteröityminen pelinjärjestäjäksi
- pelin tietojen syöttäminen &#x2713;
- ilmoittautumislomakkeen luonti &#x2713;
- kysymysten lisääminen lomakkeeseen
- uusien kysymysten luonti (kenttätyyppi + vastausvaihtoehdot)
- lomakkeen julkaiseminen &#x2713;
- täytettyjen lomakkeiden vastausten tarkastelu

### Käyttäjälle
- tunnuksen luonti &#x2713;
- palvelussa julkaistujen pelien tarkastelu &#x2713;
- ilmoittautumislomakkeen täyttäminen &#x2713;
- ilmoittautumislomakkeen lähettäminen &#x2713;

## Tarvittavat sivut / näkymät
- sisäänkirjaus &#x2713;
- rekisteröityminen &#x2713;
- omien tietojen muokkaus
- pelin luonti &#x2713;
- pelin tietojen muokkaaminen &#x2713;
- ilmoittautumislomakkeen luonti &#x2713;
- uuden kysymyksen luonti
- julkaistut pelit &#x2713;
- ilmoittautumislomakkeen täyttö &#x2713;
- vastausluettelo
- yksittäisen vastauksen tarkastelu

## Sovelluksen tietokantarakenne
![Database diagram](https://github.com/vmarttil/larp-ilmo/blob/main/images/larp-ilmo_2.png)

## Sovelluksen käyttöhje (testausversio)

Sovellus on testattavissa osoitteessa [https://larp-ilmo.herokuapp.com/](https://larp-ilmo.herokuapp.com/).

### Pääsivu

Sovelluksen pääsivulla näkyy lista sovelluksessa julkaistuista peleistä ja niiden tietoja on mahdollista
tarkastella (myös kirjautumatta sovellukseen) klikkaamalla pelin nimeä listassa. Sivun yläreunassa on linkit 
sovellukseen rekisteröitymistä ja rekisteröityneiden käyttäjien sisäänkirjautumista varten. Rekisteröitymällä
on mahdollista luoda omia pelejä ja ilmoittautua muiden luomiin peleihin.

### Pelin luonti

Sivun yläreunassa näkyy sisäänkirjautuneille käyttäjille linkki "Ilmoita peli", jonka kautta on mahdollista lisätä
sovellukseen uusi peli tietoineen ja luoda sille ilmoittautumislomake. Uuden pelin luonti -sivulla "Tallenna peli" 
tallentaa pelin tiedot, mutta ei vielä luo sille ilmoittautumislomaketta. Pelin luonut käyttäjä pääsee myöhemmin 
muokkaamaan pelin tietoja pääsivun peliluettelossa näkyvän "Muokkaa"-linkin kautta, ja tätä kautta voi myös luoda 
pelille ilmoittautumislomakkeen. 

### Ilmoittautumislomakkeen luonti

Pelin luonti- ja muokkausivun painike "Luo ilmoittautumislomake" luo pelille ilmoittautumislomakkeen ja avaa sen
näkyviin. Tässä vaiheessa lomakkeessa on oletuskysymykset, joita ei pysty vielä muokkaamaan; lopullisessa versiossa 
käyttäjä voi poistaa oletuskysymyksiä ja luoda itse uusia kysymyksiä valmiiksi määriteltyjen kenttätyyppien pohjalta 
ja lisätä niitä ilmoittautumiseen. Ilmoittautumislomakkeen muokkausnäkymän alareunassa on "Avaa ilmoittautuminen" 
-painike, joka julkaisee ilmoittautumislomakkeen siten, että kaikki sisään kirjautuneet käyttäjät pystyvät ilmoittautumaan 
peliin pääsivun listassa näkyvän "Ilmoittaudu"-linkin kautta.

### Ilmoittautuminen


