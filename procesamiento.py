import pandas
import scipy.stats as stats
import numpy as np
import plotly.express as px
from plotly.graph_objects import Figure, Bar



class Prosesamiento():
    def __init__(self, file):
        self.data = pandas.read_csv(file, encoding='latin1',
                                    parse_dates=True)
        self.columnsNumeric = self.data.describe().columns
        self.datanumeric = self.data.select_dtypes(include=["number"])
    
        self.datastring= self.data.select_dtypes(include=["object"])
        self.datatime = self.data.select_dtypes(include=["datetime"])
    
    def get_head(self):

        return self.data.head().to_html(
            classes=" forma table my-custom-table")
    
    
       
    def get_tail(self):
        return self.data.tail().to_html(
            classes=" forma table my-custom-table")
    

    def get_shape(self):
        return self.data.shape
    
    def get_nan(self):
        return (self.data.isna().values.any(), 
                self.data.isna().sum().sum())
    
    def get_duplicates(self):
        return (self.data.duplicated().values.any(),
                self.data.duplicated().sum())
    
    def get_columns_all(self):
        
        return [(self.data[column].dtype,column, self.data[column].duplicated().sum(),
                 self.data[column].isna().sum())for column in self.data.columns]
        
    def get_describe_statistics(self):
        
        informacion = []
        columns = self.columnsNumeric

        for column in columns:
           informacion.append((column,self.data[column].count(),
           self.data[column].mean(),
           self.data[column].median(),
           self.data[column].mode()[0],
           self.data[column].std(),
           self.data[column].var(),
           self.data[column].min(),
           self.data[column].max(),
           self.data[column].quantile(0.25),
           self.data[column].quantile(0.50),
           self.data[column].quantile(0.75)
           ))
   
        return informacion
    
    
    
    #### ESTO ES DE MI ESTADISTICA INFERENCIAL
    def get_statisticas_inferencial(self):
        informacion = []
        
        columns = self.columnsNumeric
        muestra = self.data.sample(frac=0.5, random_state=1)
        n = muestra.shape[0]
        confidence_level = 0.95
        z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
        
        for column in columns:
            mean_sample = muestra[column].mean()
            std_sample = muestra[column].std()
            margin_of_error = z_score*(std_sample / np.sqrt(n))
            confidence_interval = (mean_sample - margin_of_error, mean_sample + margin_of_error)
                

            informacion.append(
                (
                 column
                 ,self.data[column].mean(),
                 mean_sample,
                 self.data[column].std(),
                 std_sample,
                 confidence_interval,
                 
       
                )
            )
        
        return informacion
    def get_correlacion_spearman(self):
        return self.datanumeric.corr(method="spearman").to_html(
            classes="forma table my-custom-table")
        
    def get_correlacion_pearson(self):
        return self.datanumeric.corr(method="pearson").to_html(
            classes="forma table my-custom-table")
        
        
        
        
        
    ####HISTOGRAAMAASSSS 
    
    
    def get_histogramas(self):
        
        graficas = []
        
        
        
        for column_string in self.datastring.columns:
            
            for column_numeric in self.datanumeric.columns:
                fig = px.bar(self.data,
                            x=column_string,
                            y=column_numeric, width=910, height=500,
                            color_continuous_scale='Agsunset',
                            color=column_numeric,
                            title=f"Histograma de {column_numeric} por {column_string}",
            
                            )
            
                fig.update_layout(
                paper_bgcolor='#060D3A',  # Fondo del contenedor principal
                plot_bgcolor='white',   # Fondo del gráfico en sí
                font=dict(color='#FFC2F7'), # Color del texto para contraste,
                title_font = dict(size=25,color="#FB00E6"),
                xaxis_title_font=dict(size=18),  # Tamaño de la fuente del título del eje x
                yaxis_title_font=dict(size=18),
                xaxis={'categoryorder': 'total descending'}
            )

            graficas.append((fig.to_html(full_html=False) ))
    
        return graficas

            
        
    def histograma_images(self):
        graficas = []
        
        
        
        for column_string in self.datastring.columns:
            
            for column_numeric in self.datanumeric.columns:
                fig = px.bar(self.data,
                            x=column_string,
                            y=column_numeric, width=910, height=500,
                            color_continuous_scale='Agsunset',
                            color=column_numeric,
                            title=f"Histograma de {column_numeric} por {column_string}",
            
                            )
            
                fig.update_layout(
                paper_bgcolor='#060D3A',  # Fondo del contenedor principal
                plot_bgcolor='white',   # Fondo del gráfico en sí
                font=dict(color='#FFC2F7'), # Color del texto para contraste,
                title_font = dict(size=25,color="#FB00E6"),
                xaxis_title_font=dict(size=18),  # Tamaño de la fuente del título del eje x
                yaxis_title_font=dict(size=18),
                xaxis={'categoryorder': 'total descending'}
            )

            img_filename = f"{column_string}_{column_numeric}.png"
            fig.write_image(img_filename)
            graficas.append(img_filename)
    
        return graficas
        
        
        
     

    #### PARA EL DE CAJASS
    def get_box(self):
        graficas = []
        
        for column_string in self.datastring.columns:
            for column_numeric in self.datanumeric.columns:
                fig = px.box(self.data, x=column_string,
                             y=column_numeric, width=910, height=500,
                             title=f"Diagrama de cajas de {column_numeric} por {column_string}",
                             points="all")
                fig.update_layout(
                    paper_bgcolor='#060D3A',  # Fondo del contenedor principal
                    plot_bgcolor='white',  # Fondo del gráfico en sí
                    font=dict(color='#FFC2F7'),  # Color del texto para contraste,
                    title_font=dict(size=25, color="#FB00E6"),
                    xaxis_title_font=dict(size=18),  # Tamaño de la fuente del título del eje x
                    yaxis_title_font=dict(size=18),
                )
                graficas.append(fig.to_html(full_html=False))        
        
        return graficas
    
    
    
    
    
    #### LOS DE DISPERSION
    def get_scatter(self):
        graficas = []
        
        for column_string in self.datastring.columns:
            
            for column_numeric in self.datanumeric.columns:
                fig = px.scatter(self.data,
                            x=column_string,
                            y=column_numeric, width=910, height=500,
                            color_continuous_scale='Agsunset',
                            color=column_numeric,
                            title=f"Histograma de {column_numeric} por {column_string}",
            
                            )
            
                fig.update_layout(
                paper_bgcolor='#060D3A',  # Fondo del contenedor principal
                plot_bgcolor='white',   # Fondo del gráfico en sí
                font=dict(color='#FFC2F7'), # Color del texto para contraste,
                title_font = dict(size=25,color="#FB00E6"),
                xaxis_title_font=dict(size=18),  # Tamaño de la fuente del título del eje x
                yaxis_title_font=dict(size=18),
    
            )
            
                graficas.append(fig.to_html(full_html=False))
        
        return graficas
        
        
        
        
        
        