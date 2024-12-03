# About this software

This software allows you to create linear regression models from data sets. The models can be saved, edited, and used to generate predictions. Easily create and apply linear regression models for all your project needs. 

A suitable environment is key to running any software smoothly. This software tool was designed for a Windows environment and would work best with an operating system of Windows 10 and above. 

# Table of contents

- [Uploading your database](#uploading-your-database)
- [Datos tab overview](#datos-tab-overview)
- [Generating your model](#generating-your-model)
- [Modelo tab overview](#modelo-tab-overview)
- [Preprocessing null data](#preprocessing-null-data)
- [Adding a model description](#adding-a-model-description)
- [Saving your model](#saving-your-model)
- [Saving the graph as an image file](#saving-the-graph-as-an-image-file)
- [Upload a model file](#upload-a-model-file)
- [Creating a prediction](#creating-a-prediction)
- [Changing the interface color](#changing-the-interface-colors)
- [Graph toolbar guide](#graph-toolbar-guide)

# Uploading your database

The first step to creating a linear regression model is preparing a well-rounded set of data. Once you have gathered the data, upload your database file and begin generating models.

**To upload your database**
1. Open the software.
2. Select the **Abrir Archivo** button.<br>
The File Explorer opens.
3. Select the database file you want to upload.<br>
The database shows up in the Datos tab and an Éxito dialog appears.<br>
You have successfully uploaded your data set to the software.

# Datos tab overview

Refer to the following screenshot and table for the name and purpose of the buttons and sections found in the Datos tab.

![Datos tab screenshot](<../README images/datos tab.jpg>)

Number | Name and purpose
--- | --- 
1 | Datos tab. Shows the data uploaded.
2 | Abrir Archivo button. Uploads database files.
3 | Cargar Modelo button. Uploads model files.
4 | File name and location.
5 | Seleccione columnas de entrada (features) section. Select feature data.
6 | Seleccione columna de salida (target) section. Select target data.
7 | Confirmar selección button. Confirm your data selection.
8 | Preprocessing function buttons.

# Generating your model

Once you have uploaded your database into the software, you can begin generating linear regression models. You can generate as many models as you want, with each new model and their information appearing in a separate, numbered Modelo tab.

**To generate a model**
1. Upload a database to the software.
2. In the **Datos tab**, under the **Seleccione columnas de entrada (features)** section, select your feature data. You can choose more than one feature data.
3. Under the **Seleccione columna de salida (target)** section, choose your target data from the dropdown menu. You can only choose one target data.<br>
The selected columns are highlighted.
4. Select the **Confirmar selección** button.<br>
An Éxito dialog and Modelo tab appear.
5. Go to the **Modelo tab** and select the **Crear Modelo de Regresión Lineal** button.<br>
An Éxito dialog appears and your linear regression model is successfully generated.

> [!IMPORTANT]
> Models cannot be generated if there are null data present. An Éxito dialog shows if you have any null data. See [Preprocessing null data](#preprocessing-null-data) for more details on editing your null data.

# Modelo tab overview

Refer to the following screenshot and table for the name and purpose of the buttons and sections found in the Modelo tab.

![Modelo tab screenshot](<../README images/modelo tab.jpg>)

Number | Name and purpose
--- | --- 
1 | Modelo tab. Numbered and shows the model information.
2 | Crear Modelo de Regresión Lineal button. Generates a linear regression model.
3 | Haz clic para añadir una descripción section. Adds a model description.
4 | Predicción section. Adds new feature values.
5 | Realizar Predicción button. Creates predicted target data
6 | Guardar Modelo button. Saves the model.
7 | Visualización section. Shows the graph of the model.
8 | Graph toolbar. Edits the graph image.

# Preprocessing null data 

Depending on the data selected, you may have null data. If this happens, a row of preprocessing buttons appears so you can edit your null data directly from the software. Please make sure to preprocess all null data before generating a model.

**To preprocess null data before generating a model**
1. When null data is detected in the selected columns, confirm the Éxito dialog.<br>
A row of preprocessing function buttons appears.
2. Select the button for the function you want to apply to the null data.
3. Select the **Aplicar preprocesado** button.<br>
An Éxito dialog appears when the preprocessing function is completed.
4. Go to the **Modelo** tab and select the **Crear Modelo de Regresión Lineal** button to generate the model.<br>
You have successfully edited the null data before generating a model.

> [!NOTE]
> The following screenshot and table show the function of each null data preprocessing button.

![Preprocessing function button](<../README images/preprocessing buttons.jpg>)

Button name | Function
--- | --- 
Eliminar | Deletes the null data.
Media | Replaces null data with the mean.
Mediana | Replaces null data with the median.
Constantes | Replaces with a constant you enter.
Aplicar preprocesado | Applies the preprocessing choice to all null data in the selected columns.

# Adding a model description

If you want to differentiate between two similar models or make a note about a specific model, you can add a short description.

**To add a model description** 
1. Go to the **Modelo** tab of the model you want to add a description.
2. Select the **Haz clic para añadir una descripción** section.<br>
A cursor appears.
3. Enter your description for the model.<br>
You have successfully added a description to a model.

# Saving your model

Once you are satisfied with the model you generated, you can save it to your computer and open it in the software tool another time. Models are saved as a joblib file, and any descriptions added are saved as well.

**To save your model**
1. Go to the **Modelo** tab of the model you want to save. 
2. Select the **Guardar Modelo** button.
3. Name and save your model file with the File Explorer.<br>
You have successfully saved your model.

# Saving the graph as an image file

When you generate a model, an interactive graph of the model is also created. You can choose to save the graph as an image file to easily apply elsewhere. Please note that this method only saves an image of the graph and not the model itself.

**To save the graph as an image file**
1.	Go to the **Modelo** tab of the graph you want to save.
2.	Move the graph using the icons in the graph toolbar until your desired image appears in the Visualización section.
3.	Select the ![Save icon](<../README images/save icon.jpg>) save icon.
4.	Name and select the file type you want to save as.<br>
You have successfully saved the graph as an image file.

> [!IMPORTANT]
> Only the area of the graph shown in the Visualización section of the interface is saved. Move the graph around before saving as an image file. See the [Graph tool bar guide](#graph-tool-bar-guide) for more details on editing the graph.

# Upload a model file

You can also work with a model file with this software. Continue working on a previously saved model or use models generated by other people.

**To upload a model file**
1. In the **Datos** tab, select the **Cargar Modelo** button.<br>
The File Explorer opens.
2. Select the model file you want to use. 
A **Modelo** tab with the selected model and an Éxito dialog appears.<br>
You have successfully uploaded a model file.

# Creating a prediction

Because linear regression models are a type of machine learning algorithm, you can create predictions using this software. Using a model you have generated, add new target values to predict a feature value.

**To create a prediction**
1. Go to the **Modelo** tab of the model you want to use for prediction.
2. In the **Predicción** section, enter your new target values.
3. Select the **Realizar Predicción** button.<br>
A feature value is generated, and you have successfully created a prediction.

# Changing the interface colors

A fun feature of this software is that you can choose between four different colors themes for your interface. Switch between the themes to find the color that best suits your needs. By default, the software uses the dark pink theme.

**To change your interface color theme**
1. Select the ![Gear icon](<../README images/gear icon.jpg>) gear icon.
2. Choose a new color theme from the drop-down menu.<br>
You have successfully changed your interface color.

# Graph toolbar guide

The graph toolbar allows you to save and edit the image shown in the Visualizacion section. Refer to the following table for the purpose of each icon.

Icon | Purpose
--- | --- 
![Home icon](<../README images/home icon.jpg>) | Returns the graph to original image.
![Move icon](<../README images/move icon.jpg>) | Moves the graph left and right.
![shift icon](<../README images/shift icon.jpg>) | Moves the graph in all directions.
![Zoom icon](<../README images/zoom icon.jpg>) | Zooms in on the graph.
![Adjust value icon](<../README images/adjust value icon.jpg>) | Adjusts the graph borders and spacing.
![Figure option icon](<../README images/figure option icon.jpg>) | Adjusts the graph options such as color and axis range.
![Save icon](<../README images/save icon.jpg>) | Saves the graph as an image file.

