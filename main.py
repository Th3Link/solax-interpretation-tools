from interpret import *

# Mapping from index to corresponding data label
index_to_label = {
    0: "Spannung – L1", #Factor 10
    1: "Spannung – L2",
    2: "Spannung – L3",
    3: "Strom – L1",
    4: "Strom – L2",
    5: "Strom – L3",
    6: "Leistung – L1",
    7: "Leistung – L2",
    8: "Leistung – L3", 
    10: "PV1 Voltage Volt", #Factor 10
    11: "PV2 Voltage Volt", #Factor 10
    129: "PV3 Voltage Volt", #Factor 10
    12: "PV1 Current Ampere", #Factor 10
    13: "PV2 Current Ampere", #Factor 10
    130: "PV3 Current Ampere", #Factor 10
    14: "PV1 Power Watt", #Factor 1
    15: "PV2 Power Watt", #Factor 1
    131: "PV3 Power Watt", #Factor 1
    16: "L1-Frequenz Hz",
    17: "L2-Frequenz Hz",
    18: "L3-Frequenz Hz",
    19: "Run mode - normal",
    34: "Grid Power",
    39: "Battery Voltage",
    70: 'Tagesertrag On-Grid (kWh)', #Factor 10
    58: 'Gesamtertrag On-Grid (kWh)', #Factor 10
    86: 'Summierte Netzeinspeisung (kWh)', #Factor 100
    88: 'Summierte Netzausspeisung (kWh)', #Factor 100
    159: 'AC Leistung Wechselrichter(W)', #Factor 10
}

def query_cloud():
    # Placeholder for file path
    file_path = "data/H3BC25XXXXXXXX/data.txt"
    timestamps_s, measurements_s = load_samples(file_path)
    
    # Read the Excel file into a pandas DataFrame
    timestamps_e, measurements_e = load_excel('data/H3BC25XXXXXXXX/cloud.xls')
    
    comparison_results = compare_all_sequences(
        timestamps_e,
        remove_zero_measurements(measurements_e),
        timestamps_s,
        remove_zero_measurements(measurements_s))
        
    plot_comparison_results(
        ["Gesamtertrag (kWh)",
            "Tagesertrag (kWh)",
            "feed-in energy(kWh)",
            "PV2 Spannung (V)",
            "PV2 Strom (A)",
            "PV2 Eingangsleistung (W)",
            "AC Strom R(A)",
            "Ausgangs Leistung (W)",
            "consume energy(kWh)",
            "Einspeiseleistung (W)",
        ],
        comparison_results)

def query_manual():
    # Placeholder for file path
    file_path = "data/H3BC25XXXXXXXX/data.txt"
    timestamps_s, measurements_s = load_samples(file_path)
    
    # Read the Excel file into a pandas DataFrame
    timestamps_e, measurements_e = load_excel('data/H3BC25XXXXXXXX/manual.xls')
    
    comparison_results = compare_all_sequences(
        timestamps_e,
        remove_zero_measurements(measurements_e),
        timestamps_s,
        remove_zero_measurements(measurements_s))
        
    plot_comparison_results(
        ["PV1 Amps",
            "PV2 Amps",
            "PV3 Amps",
            "PV1 Volts",
            "PV2 Volts",
            "PV3 Volts",
            "PV1 Watt",
            "PV2 Watt",
            "PV3 Watt",
            "Ausgangsstrom L1",
            "Ausgangsstrom L2",
            "Ausgangsstrom L3",
            "Netzspannung L1",
            "Netzspannung L2",
            "Netzspannung L3",
            "On-Grid Tagesertrag (kWh)",
            "On-grid Gesamtertrag (kWh)",
            "Netzleistung Watt",
            "Summierte Netzeinspeisung (kWh)",
            "Summe Netzausspeisung (kWh)",
            "AC-Leistung Wechselrichter Watt",
        ],
        comparison_results)

def main():
    query_cloud()

if __name__ == "__main__":
    main()

