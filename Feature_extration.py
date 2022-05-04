from radiomics import featureextractor, getFeatureClasses
from __future__ import print_function
import SimpleITK as sitk
import pandas as pd
import numpy as np
import radiomics
import logging
import nrrd
import six
import os

# Leitura do arquivo NRRD com a característica e coloca numa matriz
def readNrrdData(filename): 
    data, header = nrrd.read(filename)
    voxels = []
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
          for z in range(data.shape[2]):
            if not np.isnan(data[x, y, z]):
                voxels.append(data[x, y, z])
    return voxels

# Caminho do arquivo de configuração YAML
paramsFile = "C:/..."

# Pasta com as imagens
pasta = " C:/..."

# Extrator
extractor = featureextractor.RadiomicsFeatureExtractor(paramsFile)
featureClasses = getFeatureClasses()

# Extração de características Radiômicas por voxel
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        f_name = arquivo.split('.') 
        features_dir = diretorio+'\\'+f_name[0]
        try:
            mask = "C:/..." + arquivo
            image = diretorio+'/'+arquivo
            featureVector = extractor.execute(image, mask, voxelBased=True)
            for featureName, featureValue in six.iteritems(featureVector):
                if isinstance(featureValue, sitk.Image):
                    sitk.WriteImage(featureValue, "C:/..." +'/%s-%s.nrrd'%(f_name[0], featureName)) #coloca o resultado da extração da feature num arquivo nrrd
        except OSError as error:
            pass

# Diretorio com os arquivos NRRD contendo o resultado
pasta = r"C:/..."

for diretorio, subpastas, arquivos in os.walk(pasta): 
    df = pd.DataFrame()
    patient_code = ''
    for arquivo in arquivos:
        split = arquivo.split('-')
        # Id
        patient_code = split[0] 
        
        # Nome da feature
        feature_name = split[1].split('.nrrd') 
        features = readNrrdData(diretorio+'/'+arquivo)
        
        # Coloca a matriz num dataframe
        df[feature_name[0]] = pd.Series(features) 
        
        # Exporta as features para csv
        df.to_csv("C:/..." + patient_code+'_features.csv', index = False)