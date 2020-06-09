import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import pickle
import xgboost as xgb

filename = 'rf.sav'
model = pickle.load(open("clf.dat", "rb"))
scaler = pickle.load(open("scaler.dat", "rb"))


@st.cache
def dif_dias(data_sintomas):
    hoje = date.today().day
    dif_dias = int(str(hoje - data_sintomas.day))
    return dif_dias

def main():

    st.title('Predição de diagnóstico do COVID-19')
    idade = st.number_input('Idade', step=1,max_value=130,min_value=0,value=0)
    sexo = st.radio('Sexo',['Masculino','Feminino'])
    if sexo == 'Masculino':
        sexo_cat = 1
    else:
        sexo_cat = 0


    observacoes = st.multiselect('Selecione as especificidades deste caso', ['Profissional da Saúde',
                                                                             'Viagem dentro do país',
                                                                             'Viagem internacional',
                                                                             'Contato suspeito',
                                                                             'Gestante'])

    if 'Profissional da Saúde' in observacoes:
        profissional_saude = 1
    else: profissional_saude = 0
    if 'Viagem dentro do país' in observacoes:
        viagem_nacional = 1
    else: viagem_nacional = 0
    if 'Viagem internacional' in observacoes:
        viagem_internacional = 1
    else: viagem_internacional = 0
    if 'Contato suspeito' in observacoes:
        contato_suspeito = 1
    else:contato_suspeito = 0
    if 'Gestante' in observacoes:
        gestante = 1
    else:gestante = 0

    #profissional_saude = st.radio('Profissional da Saúde?',['Sim','Não'])
    #viagm_internacional = st.radio('Viagem Internacional?', ['Sim', 'Não'])
    #viagem_nacional = st.radio('Viagem dentro do Brasil?', ['Sim', 'Não'])
    #contato_suspeito = st.radio('Contato com alguém suspeito de estar infectado?', ['Sim', 'Não'])

    data_sintomas = st.date_input('Data dos primeiros sintomas', )
    sintomas = st.multiselect('Sintomas',['Adinamia (fraqueza)', 'Batimento da asa do nariz', 'Cefaleia ', 'Cianose', 'Coma',
                               'Congestão nasal ou conjuntival', 'Conjuntivite', 'Convulsão ', 'Coriza', 'Diarréia',
                               'Dificuldade de Respirar', 'Dispenia', 'Dor na Garganta',
                               'Exsudato faríngeo', 'Febre','Irritabilidade/Confusão', 'Mialgia', 'Náuseas/Vômito',
                               'Produção de escarro', 'Saturação O2 <95%', 'Tiragem intercostal', 'Tosse'])

    #adinamia = nariz = cefaleia = cianose = coma = congestao = conjutivite = convulsao = coriza = diarreia = respirar=0
    #engolir = dispneia  = garganta = exsudato = febre = mialgia = vomito = escarro = saturacao = tiragem = tosse = 0


    if 'Adinamia (fraqueza)' in sintomas:
        adinamia = 1
    else: adinamia = 0
    if 'Batimento da asa do nariz' in sintomas:
        nariz = 1
    else: nariz = 0
    if 'Cefaleia' in sintomas:
        cefaleia = 1
    else: cefaleia = 0
    if 'Cianose' in sintomas:
        cianose = 1
    else: cianose = 0
    if 'Coma' in sintomas:
        coma = 1
    else: coma = 0
    if 'Congestão nasal ou conjuntival' in sintomas:
        congestao = 1
    else: congestao = 0
    if 'Conjuntivite' in sintomas:
        conjutivite = 1
    else: conjutivite = 0
    if 'Convulsão' in sintomas:
        convulsao = 1
    else: convulsao = 0
    if 'Coriza' in sintomas:
        coriza = 1
    else: coriza = 0
    if 'Diarréia' in sintomas:
        diarreia = 1
    else: diarreia = 0
    if 'Dificuldade de Respirar' in sintomas:
        respirar = 1
    else: respirar = 0
    if 'Dispenia' in sintomas:
        dispneia = 1
    else: dispneia = 0
    if 'Dor na Garganta' in sintomas:
        garganta = 1
    else: garganta = 0
    if 'Exsudato faríngeo' in sintomas:
        exsudato = 1
    else: exsudato = 0
    if 'Febre' in sintomas:
        febre = 1
    else: febre = 0
    if 'Irritabilidade/Confusão' in sintomas:
        irritabilidade = 1
    else: irritabilidade = 0
    if 'Mialgia' in sintomas:
        mialgia = 1
    else: mialgia = 0
    if 'Náuseas/Vômito' in sintomas:
        vomito = 1
    else: vomito = 0
    if 'Produção de escarro' in sintomas:
        escarro = 1
    else: escarro = 0
    if 'Saturação O2 <95%' in sintomas:
        saturacao = 1
    else: saturacao=0
    if 'Tiragem intercostal' in sintomas:
        tiragem = 1
    else: tiragem = 0
    if 'Tosse' in sintomas:
        tosse = 1
    else: tosse = 0

    comorbidades = st.multiselect('Comorbidades', ['Cirurgia Bariátrica','Doença Pulmonar Crônica','Doença Cardiovascular Crônica, incluindo hipertensão',
                                    'Doença Renal Crônica','Doença Neurológica Crônica','Doença Hepática Crônica','Diabetes Mellitus',
                                    'Imunodeficiência','Infecção pelo HIV','Neoplasia','Obesidade','Tabagismo','Tuberculose'])

    pulmonar = cardio = renal = hepatica = diabetes = imuno = hiv = neoplasia = tabagismo = 0


    if 'Cirurgia Bariátrica' in comorbidades:
        bariatrica = 1
    else: bariatrica = 0
    if 'Obesidade' in comorbidades:
        obesidade = 1
    else: obesidade = 0
    if 'Tuberculose' in comorbidades:
        tuberculose = 1
    else: tuberculose = 0
    if 'Doença Pulmonar Crônica' in comorbidades:
        pulmonar = 1
    else: pulmonar = 0
    if 'Doença Cardiovascular Crônica, incluindo hipertensão' in comorbidades:
        cardio = 1
    else: cardio = 0
    if 'Doença Renal Crônica' in comorbidades:
        renal = 1
    else: renal = 0
    if 'Doença Hepática Crônica' in comorbidades:
        hepatica = 1
    else: hepatica = 0
    if 'Doença Neurológica Crônica' in comorbidades:
        neuro = 1
    else: neuro = 0
    if 'Diabetes Mellitus' in comorbidades:
        diabetes = 1
    else: diabetes = 0
    if 'Imunodeficiência' in comorbidades:
        imuno = 1
    else: imuno = 0
    if 'Infecção pelo HIV' in comorbidades:
        hiv = 1
    else: hiv = 0
    if 'Neoplasia' in comorbidades:
        neoplasia = 1
    else: neoplasia = 0
    if 'Tabagismo' in comorbidades:
        tabagismo = 1
    else: tabagismo = 0

    array = np.array([dif_dias(data_sintomas), idade, profissional_saude, febre, respirar, nariz, tiragem, cianose, saturacao,
             coma,tosse, escarro, congestao, coriza, garganta, diarreia, vomito, cefaleia, irritabilidade,
             adinamia, exsudato, conjutivite, convulsao, contato_suspeito, viagem_nacional, viagem_internacional,
             pulmonar, cardio, renal,hepatica, diabetes, imuno, hiv, neoplasia,tabagismo,bariatrica,obesidade,tuberculose,
             neoplasia, neuro,dispneia, mialgia, sexo_cat,gestante])

    df = pd.DataFrame(array).T
    colunas = ['DIF_DIAS', 'NU_IDADE_N', 'IS_PROFISSIONAL_SAUDE', 'SINT_FEBRE', 'SINT_DIF_RESP', 'SINT_NARIZ',
                   'SINT_TIRAG', 'SINT_CIAN', 'SINT_SAT', 'SINT_COMA', 'SINT_TOSSE', 'SINT_ESCA', 'SINT_CONG_NAZ',
                   'SINT_CORIZA', 'SINT_GARGANTA', 'SINT_DIARREIA', 'SINT_NAUZ', 'SINT_CEFALEIA', 'SINT_IRRITABI',
                   'SINT_ADINAMIA', 'SINT_EXSUDATO', 'SINT_CONJUT', 'SINT_CONVULSAO', 'CONTATO_SUSP', 'VIAGEM_BRASIL',
                   'VIAGEM_INTERNACIONAL', 'COMORB_PULM', 'COMORB_CARDIO', 'COMORB_RENAL', 'COMORB_HEPAT',
                   'COMORB_DIABE', 'COMORB_IMUN', 'COMORB_HIV', 'COMORB_NEOPL', 'COMORB_TABAG',
                   'COMORB_CIRURGIA_BARIAT', 'COMORB_OBESIDADE', 'COMORB_TUBERCULOSE', 'COMORB_NEOPLASIAS',
                   'COMORB_NEURO_CRONICA', 'SINT_DISPNEIA', 'SINT_MIALGIA', 'CS_SEXO_Masculino', 'CS_GESTANT_1']

    df.columns = colunas
    df = pd.DataFrame(scaler.transform(df), columns=colunas)

    pred = model.predict_proba(df)
    predicted = (pred[:, 1] >= 0.15).astype('int')
    #st.subheader('Probabilidade')
    #st.write(pred[:,1])
    st.subheader('Predição:')
    if predicted == 1:
        st.write('Positivo')
    else:
        st.write('Negativo')
if __name__ == '__main__':
    main()