import matplotlib.pyplot as plt
import pandas as pd
# Load the results from the CSV file
results_df = pd.read_csv(r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7126\job_advertisement_growth.csv')


# Extract the years and matched tools columns
years = results_df['Year'].values
matched_tools = results_df.columns[1:]

# Calculate the total number of tools matched for each year
total_matched_per_year = results_df.iloc[:, 1:].sum(axis=1).values

# Calculate the number of different tools matched for each year
different_tools_per_year = results_df.iloc[:, 1:].gt(0).sum(axis=1).values

# Create line graphs for both statistics
plt.figure(figsize=(12, 6))

# Plot the total number of tools matched for each year
plt.plot(years, total_matched_per_year, marker='o', linestyle='-', label='Total Tools Matched', color='blue')

# Plot the number of different tools matched for each year
plt.plot(years, different_tools_per_year, marker='o', linestyle='-', label='Different Tools Matched', color='green')

# Add labels and legends
plt.title('Total vs. Different Tools Matched for Each Year (2015-2022)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()

# Save the plot as an image
image_path = r'C:\Users\Vishwas\Desktop\Thesis\ontology_translation\Job_Data\Computer Science Domain New Data\7126\job_advertisement_growth.png'
plt.grid(True)
plt.tight_layout()
plt.savefig(image_path)

# Show the plot (optional)
plt.show()

# Print the path where the image is saved
print(f"Image saved at: {image_path}")
