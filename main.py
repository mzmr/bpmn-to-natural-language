# Bezokolicznik                         - INF - Infinitive
# Rzeczownik odczasownikowy             - GER - Gerund
# Tryb rozkazujący                      - IMP - Imperative mood
#
# Mianownik (kto? co?)                  - NOM - Nominative case, subjective case, straight case, upright case
# Dopełniacz (kogo? czego?)             - GEN - Genitive case, second case
# Celownik (komu? czemu?)               - DAT - Dative case
# Biernik (kogo? co?)                   - ACC - Accusative case
# Narzędnik ((z) kim? (z) czym?)        - INS - Instrumental case
# Miejscownik (o kim? o czym?)          - LOC - Locative case
# Wołacz (zwrot do kogoś lub czegoś)    - VOC - Vocative case
#
import morfeusz2
morf = morfeusz2.Morfeusz()

print(morf.dict_id())

for text in (u'Później kierowca odbierze zapłatę.', u'Kolejny krok, to dostarczenie towaru przez kierowcę.', u'Samochody jadą.', u'Na początku kierowca musi przyjąć mandat'):
    print(text)
    analysis = morf.analyse(text)

    for interpretation in analysis:
        print(interpretation)
#
#
print('-------------------------------------')
for text in morf.generate('odebrać'):
    print(text[0] + ' - ' + text[2])


print('aaa')
#
# new_sentence = Inflector().generate_first_sentence('sprzedawca', 'Znajdź żądany przedmiot')
# print(new_sentence)
#
# print("--------------------------")


from translator import Translator

# ELEMENTY W TAGU <PROCESS> MUSZĄ BYĆ W KOLEJNOŚCI, KTÓRĄ WSKAZUJĄ STRZAŁKI,
# INACZEJ STRZAŁKI ZOSTANĄ NARYSOWANE ODWROTNIE

translator = Translator('./examples/good/pizza-pl.bpmn')
translation = translator.translate()

print('======= Opis modelu: =======')

for idx, t in enumerate(translation):
    print(f'\n>>> {idx + 1} <<<')

    for sen_idx, sentence in enumerate(t):
        print(f'{sen_idx + 1}. {sentence}')
