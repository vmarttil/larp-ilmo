
/* Inserting default data into the database */

INSERT INTO FieldType (
    name
    )
    VALUES 
        ('StringField'),
        ('IntegerField'),
        ('RadioField'), 
        ('SelectField'),
        ('SelectMultipleField'),
        ('TextAreaField'),
        ('CheckboxListField');

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
        (1,'Puhelinnumero','Puhelinnumero, josta ilmoittautujan tavoittaa tarvittaessa.',true, true, null),
        (2,'Ikä','Ilmoittautujan ikä pelin aikaan.',true, true, 'age'),
        (6,'Kuvaile itseäsi pelaajana','Kuvaile pelityyliäsi ja -mieltymyksiäsi, minkä tyyppisestä pelisisällöstä yleensä nautit, oletko enemmän aktiivinen vai reaktiivinen pelaaja, jne.',true, true, 'profile'),
        (3,'Hahmon toivottu sukupuoli','Sukupuoli jota edustavaa hahmoa haluat pelata (ei välttämättä sama kuin pelaajan sukupuoli).',true, true, null),
        (7,'Kolme sinulle tärkeintä elementtiä pelissä','Valitse kolme elementtiä, joita toivot pelisi eniten sisältävän.',true, true, null),
        (7,'Teemat, joita et halua pelata','Valitse ne teemat, joita et halua hahmossasi käsiteltävän tai joita et halua pelisisältöösi.',true, true, null),
        (6,'Minkä tyyppistä hahmoa haluaisit pelata tässä pelissä?','Kuvaile vapaasti, minkälaisia ominaisuuksia, luonteenpiirteitä, tms. toivoisit hahmollesi, minkälaisessa asemassa toivoisit hahmon olevan, jne.',true, true, null),
        (6,'Minkä tyyppisiä juonikuvioita tai teemoja toivoisit peliisi?','Kuvaile minkä tyyppistä pelisisältöä haluaisit pelata ja kerro mahdollisista juoni-ideoista jollaisia haluaisit pelata.',true, true, null),
        (6,'Muita terveisiä pelinjohdolle','Tähän voit kirjoittaa ilmoittautumistasi koskevia huomioita pelinjohdolle ja muita olennaiseksi katsomiasi seikkoja, jotka eivät sopineet muihin kenttiin.',true, true, null);

INSERT INTO Option (
    option_text
    )
    VALUES
        ('Mies'),
        ('Nainen'),
        ('Muu'),
        ('Ei väliä'),
        ('Seikkailu'),
        ('Romantiikka'),
        ('Parisuhde'),
        ('Ystävyys'),
        ('Juonittelu'),
        ('Toiminta'),
        ('Politiikka'),
        ('Vastoinkäymiset'),
        ('Yllätykset'),
        ('Läheisen kuolema'),
        ('Fyysinen väkivalta'),
        ('Seksuaalisuus'),
        ('Alistaminen'),
        ('Yksinäisyys'),
        ('Henkinen väkivalta'),
        ('Mielenterveysongelmat'),
        ('Fyysiset vammat');

INSERT INTO QuestionOption (
    question_id,
    option_id
    )
    VALUES
        (6,1),
        (6,2),
        (6,3),
        (6,4),
        (7,5),
        (7,6),
        (7,7),
        (7,8),
        (7,9),
        (7,10),
        (7,11),
        (7,12),
        (7,13),
        (8,14),
        (8,15),
        (8,16),
        (8,17),
        (8,18),
        (8,19),
        (8,20),
        (8,21);

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
        )

INSERT INTO GameOrganiser (
    person_id,
    game_id
    ) VALUES (
        1,
        1
    )

INSERT INTO Form (
    name
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