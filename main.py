import processor
import visualisation
import analysis

data_class = processor.Data()
data_class.basic_info
data = data_class.get_data()

analysis.do_analysis()