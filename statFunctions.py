import numpy as np
from PIL import Image
from skimage.feature import graycomatrix
from skimage.metrics import structural_similarity 
import cv2

def autocorrelation_x_normalized(image_path, shift):
    # Charger l'image
    image = Image.open(image_path)
    
    # Conversion de l'image en niveaux de gris
    gray_image = image.convert('L')
    # Conversion de l'image en tableau numpy
    gray_array = np.array(gray_image, dtype=np.float32)

    # Décalage de l'image horizontalement
    shifted_array = np.roll(gray_array, shift, axis=1)
        
    # Calcul de la corrélation entre l'image d'origine et l'image décalée
    correlation = np.mean(gray_array * shifted_array)

    # Normalisation en divisant par la variance de l'image
    correlation_normalized = correlation / np.var(gray_array)

    return correlation_normalized

def image_correlation(image1, image2):
   
    # On resize les images au cas où
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    correlation_coefficient = np.corrcoef(image1.flatten(), image2.flatten())[0, 1]
    return correlation_coefficient

def image_mean_squared_error(image1, image2):
   
    # On resize les images au cas où
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    mse = np.mean((image1 - image2) ** 2)
    return mse

def image_energy_contour(image):
    # Convertir l'image en echelles de gris
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculer les gradients horizontaux et verticaux
    gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    
    # Calculer l'énergie des gradients en utilisant la somme des carrés des gradients
    energy_matrix = np.sqrt(gradient_x**2 + gradient_y**2)
    energy_global = np.sum(energy_matrix)
    return energy_matrix, energy_global

def image_contrast(image):
    
    contrast = 0

    glcm = image_glcm(image)
    for i in range(len(glcm)):
        for j in range(len(glcm)):
            contrast += glcm[i][j]*((i-j)**2)
    return contrast

def image_glcm(image):
    #image = cv2.imread(image,0)
    glcm = graycomatrix(image, distances=[5], angles=[0], levels=256,symmetric=True, normed=True)
    return glcm

def image_homogeneity(image):
    homogeneity = 0

    glcm = image_glcm(image)
    for i in range(len(glcm)):
        for j in range(len(glcm)):
            homogeneity += glcm[i][j] / (1 + (i-j)**2)
    return homogeneity

def image_ssim(image1, image2):

    # On resize les images au cas où
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    image1_np = np.array(image1)
    image2_np = np.array(image2)

    # Calculer le SSIM
    ssim_value, _ = structural_similarity(image1_np, image2_np, full=True)

    return ssim_value

def correlations(images):
    correlations = np.zeros((5, 3, 3))
    for f in range(len(images)):
        #print("Corrélations entre images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            for  j in range(i+1, len(images[f])):
                image1 = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
                image2 = cv2.imread(images[f][j], cv2.IMREAD_GRAYSCALE)
                correlations[f, i, j] = image_correlation(image1, image2)
                correlations[f, j, i] = correlations[f, i, j]
                #print(f"La corrélation entre {natures[i]} et {natures[j]} est : {correlations[f, i, j]}")
    return correlations

def mean_squared_errors(images):
    mse = np.zeros((5, 3, 3))
    for f in range(len(images)):
        #print("Les erreurs quadratiques moyennes entre images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            for  j in range(i+1, len(images[f])):
                image1 = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
                image2 = cv2.imread(images[f][j], cv2.IMREAD_GRAYSCALE)
                mse[f, i, j] = image_mean_squared_error(image1, image2)
                mse[f, j, i] = mse[f, i, j]
                #print(f"La mse entre {natures[i]} et {natures[j]} est : {mse[f, i, j]}")
    return mse

def energies(images):
    energies = np.zeros((5, 3))
    for f in range(len(images)):
        #print("Les energies par image pour le filtre : ", f+1)
        for i in  range(len(images[f])):
            #print(f"Energie de l'image : {natures[i]}")
            image = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
            #energie = image_energy_contour(image)[0]
            energies[f,i] = image_energy_contour(image)[1]
            #print(f"L'energie de l'image {natures[i]} est : {energies[f,i]}") 
            # Appliquer une amplification des contours à l'image d'énergie
            #amplification_factor = 2.0
            #amplified_energie = energie * amplification_factor

            # Afficher l'image d'énergie originale
            #cv2.imshow('Energie des gradients originale', energie.astype(np.uint8))

            # Afficher l'image d'énergie avec les contours accentués
            #cv2.imshow('Contours accentués (Energie des gradients)', amplified_energie.astype(np.uint8))
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #energies[f, i] = image_energy(image)
            #print(f"L'energie de l'image ' {natures[i]} est : {energies[f, i]}")
    return energies

def autocorrelations(images):
    autocorrelations = np.zeros((5, 3))
    shift = 10
    for f in range(len(images)):
        #print("Contrastes des images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            autocorrelations[f, i] = autocorrelation_x_normalized(images[f][i], shift)
            #print(f"Le contraste de l'image {natures[i]} est : {contrasts[f, i]}")
    return autocorrelations

def contrasts(images):
    contrasts = np.zeros((5, 3))
    for f in range(len(images)):
        #print("Contrastes des images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            image = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
            contrasts[f, i] = image_contrast(image)[0, 0]
            #print(f"Le contraste de l'image {natures[i]} est : {contrasts[f, i]}")
    return contrasts

def homogeneities(images):
    homogeneities = np.zeros((5, 3))
    for f in range(len(images)):
        #print("Homogeneites des images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            image = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
            homogeneities[f, i] = image_homogeneity(image)[0, 0]
            #print(f"L'homogeneite de l'image {natures[i]} est : {homogeneities[f, i]}")
    return homogeneities

def ssim(images):
    ssim = np.zeros((5, 3, 3))
    for f in range(len(images)):
        #print("SSIM entre images pour filtre : ", f+1)
        for i in  range(len(images[f])):
            for  j in range(i+1, len(images[f])):
                image1 = cv2.imread(images[f][i], cv2.IMREAD_GRAYSCALE)
                image2 = cv2.imread(images[f][j], cv2.IMREAD_GRAYSCALE)
                ssim[f, i, j] = image_ssim(image1, image2)
                ssim[f, j, i] = ssim[f, i, j]
                #print(f"La ssim entre {natures[i]} et {natures[j]} est : {ssim[f, i, j]}")
    return ssim

