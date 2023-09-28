# Set the 'Year' column as the index
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
results_df = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7126\job_advertisement_growth.csv')


results_df.set_index('Year', inplace=True)

# Transpose the DataFrame to have matched tools as columns
#results_df = results_df.transpose()

# Create a custom color palette
custom_palette = sns.color_palette("husl", len(results_df.columns))

# Create the stacked bar plot using Seaborn with the custom color palette
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

ax = results_df.plot(kind='bar', stacked=True, color=custom_palette, figsize=(12, 6))
plt.title('Stacked Bar Plot of Matched Tools by Year (2015-2022)')
plt.xlabel('Year')
plt.ylabel('Count')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Customize legend (optional)
legend_labels = [plt.Line2D([0], [0], color=custom_palette[i], lw=4, label=tool)
                 for i, tool in enumerate(results_df.columns)]
plt.legend(handles=legend_labels, title='Matched Tools', loc='upper left', bbox_to_anchor=(1, 1))

# Save the plot as an image
image_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7126\stacked_bar_plot_2.png'
plt.tight_layout()
plt.savefig(image_path, bbox_inches='tight')

# Show the plot (optional)
plt.show()

# Print the path where the image is saved
print(f"Stacked Bar Plot saved at: {image_path}")
