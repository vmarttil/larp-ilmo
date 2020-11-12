# larp-ilmo

## Web-sovellus liveroolipelien ilmoittautumislomakkeiden luomiseen ja täyttämiseen

Sovellus tarjoaa liveroolipelien järjestäjille mahdollisuuden rekisteröityä palveluun pelinjärjestäjiksi ja luoda peliään varten mukautetuu ilmoittautumislomake käyttäen hyväksi sekä valmiiksi luotuja vakiokysymyksiä että valmiiksi määriteltyjen kenttätyyppien (esim. vapaa tekstivastaus, monivalinta, samaa mieltä / eri mieltä -asteikko) pohjalta itse luomiaan kysymyksiä ja julkaista lomake täytettäväksi. Muut käyttäjät voivat täyttää ilmoittautumislomakkeen ja tallentaa sen tietokantaan, jossa kyseisen pelin järjestäjä voi tarkastella täytettyjä ilmoittautumisia.

## Sovelluksen toiminnallisuudet

### Pelinjärjestäjälle

- tunnuksen luonti
- rekisteröityminen pelinjärjestäjäksi
- pelin tietojen syöttäminen
- ilmoittautumislomakkeen luonti
- kysymysten lisääminen lomakkeeseen
- uusien kysymysten luonti (kenttätyyppi + vastausvaihtoehdot)
- lomakkeen julkaiseminen
- täytettyjen lomakkeiden vastausten tarkastelu

### Käyttäjälle
- tunnuksen luonti
- palvelussa julkaistujen pelien tarkastelu
- ilmoittautumislomakkeen täyttäminen
- ilmoittautumislomakkeen lähettäminen

## Tarvittavat sivut / näkymät
- sisäänkirjaus
- rekisteröityminen / omien tietojen muokkaus
- pelin luonti / tietojen täyttäminen
- ilmoittautumislomakkeen luonti
- uuden kysymyksen luonti
- julkaistut pelit
- ilmoittautumislomakkeen täyttö
- vastausluettelo
- yksittäisen vastauksen tarkastelu

## Sovelluksen tietokantarakenne
![Database diagram](https://github.com/vmarttil/larp-ilmo/blob/main/images/larp-ilmo.png)
