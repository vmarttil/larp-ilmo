
/* Inserting default data into the database */

INSERT INTO FieldType (
    name,
    display
    )
    VALUES 
        ('StringField', 'Tekstikenttä'),
        ('IntegerField', 'Numerokenttä'),
        ('RadioField', 'Valintanappi'), 
        ('SelectField', 'Valitsin'),
        ('SelectMultipleField', 'Monivalitsin'),
        ('TextAreaField', 'Tekstialue'),
        ('CheckboxListField', 'Valintaruutu');

INSERT INTO Question (
    field_type, 
    question_text, 
    description, 
    is_default,
    is_optional,
    prefill_tag
    )
    VALUES
        (1,'Nimi','Ilmoittautujan koko nimi.',true, false, 'name'),
        (1,'Sähköposti','Sähköpostiosoite johon peliin liittyvät tiedotteet lähetetään.',true, false, 'email'),
        (1,'Puhelinnumero','Puhelinnumero, josta ilmoittautujan tavoittaa tarvittaessa.',true, true, 'phone'),
        (2,'Ikä','Ilmoittautujan ikä pelin aikaan.',true, true, 'age'),
        (6,'Kuvaile itseäsi pelaajana','Kuvaile pelityyliäsi ja -mieltymyksiäsi, minkä tyyppisestä pelisisällöstä yleensä nautit, oletko enemmän aktiivinen vai reaktiivinen pelaaja, jne.',true, true, 'profile'),
        (3,'Hahmon toivottu sukupuoli','Sukupuoli jota edustavaa hahmoa haluat pelata (ei välttämättä sama kuin pelaajan sukupuoli).',true, true, null),
        (7,'Kolme sinulle tärkeintä elementtiä pelissä','Valitse kolme elementtiä, joita toivot pelisi eniten sisältävän.',true, true, null),
        (7,'Teemat, joita et halua pelata','Valitse ne teemat, joita et halua hahmossasi käsiteltävän tai joita et halua pelisisältöösi.',true, true, null),
        (6,'Minkä tyyppistä hahmoa haluaisit pelata tässä pelissä?','Kuvaile vapaasti, minkälaisia ominaisuuksia, luonteenpiirteitä, tms. toivoisit hahmollesi, minkälaisessa asemassa toivoisit hahmon olevan, jne.',true, true, null),
        (6,'Minkä tyyppisiä juonikuvioita tai teemoja toivoisit peliisi?','Kuvaile minkä tyyppistä pelisisältöä haluaisit pelata ja kerro mahdollisista juoni-ideoista jollaisia haluaisit pelata.',true, true, null),
        (6,'Muita terveisiä pelinjohdolle','Tähän voit kirjoittaa ilmoittautumistasi koskevia huomioita pelinjohdolle ja muita olennaiseksi katsomiasi seikkoja, jotka eivät sopineet muihin kenttiin.',true, true, null);

INSERT INTO Option (
    question_id,
    option_text
    )
    VALUES
        (6,'Mies'),
        (6,'Nainen'),
        (6,'Muu'),
        (6,'Ei väliä'),
        (7,'Seikkailu'),
        (7,'Romantiikka'),
        (7,'Parisuhde'),
        (7,'Ystävyys'),
        (7,'Juonittelu'),
        (7,'Toiminta'),
        (7,'Politiikka'),
        (7,'Vastoinkäymiset'),
        (7,'Yllätykset'),
        (8,'Läheisen kuolema'),
        (8,'Fyysinen väkivalta'),
        (8,'Seksuaalisuus'),
        (8,'Alistaminen'),
        (8,'Yksinäisyys'),
        (8,'Henkinen väkivalta'),
        (8,'Mielenterveysongelmat'),
        (8,'Fyysiset vammat');

INSERT INTO Game (
    name, 
    start_date,
    end_date,
    location,
    price,
    description
    ) VALUES (
        'Testipeli',
        DATE '2021-05-21',
        DATE '2021-05-21',
        'Helsinki',
        35,
        'Tässä on lyhyt kuvaus pelistä.'
        );

INSERT INTO GameOrganiser (
    person_id,
    game_id
    ) VALUES (
        1,
        1
    );

INSERT INTO Form (
    game_id,
	name, 
	published
    ) 
    VALUES
    (1, 'Oletuslomake', False);

INSERT INTO FormQuestion (
    form_id,
    question_id,
    position
    )
    VALUES
    (1,1,1),
    (1,2,2),
    (1,3,3),
    (1,4,4),
    (1,5,5),
    (1,6,6),
    (1,7,7),
    (1,8,8),
    (1,9,9),
    (1,10,10),
    (1,11,11);