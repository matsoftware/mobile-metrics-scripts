//
//  CarbonIntensityView.swift
//  CarbonIntensity
//
//  Created by Mattia Campolese on 14/11/2020.
//

import DataProvider
import SwiftUI

public struct CarbonIntensityView: View {
        
    @ObservedObject var viewModel: CarbonIntensityViewModel = CarbonIntensityViewModel()
    
    public init() {}
    
    public var body: some View {
        NavigationView {
            VStack {
                Text("The carbon intensity of electricity is defined as the number of grams of carbon dioxide (CO2) that it takes to make one unit of electricity a kilowatt per hour (kW/hour). The lower the carbon intensity, the greener the electricity.")
                Button(action: {
                    UIApplication.shared.open(URL(string: "https://www.pexels.com/photo/black-ship-on-body-of-water-screenshot-929382/?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels")!, options: [:], completionHandler: nil)
                }) {
                    Assets.carbon.resizable().scaledToFit()
                }
                if let intensity =  viewModel.carbonIntensity {
                    Text("State of the Carbon Index as of now")
                        .padding()
                    Text("Forecast:  \(intensity.intensity.forecast) gCO2/kWH")
                    Text("Actual:  \(intensity.intensity.actual) gCO2/kWH")
                    Text("Index:  \(intensity.intensity.index.rawValue)")
                } else {
                    Text("No data available")
                }
                Spacer()
            }
            .padding()
            .navigationTitle("Carbon Index UK")
            .toolbar(content: {
                Button("Refresh") {
                    viewModel.loadIntensities()
                }
            })
        }
        .onAppear {
            viewModel.loadIntensities()
        }
        .alert(isPresented: $viewModel.showError) {
            Alert(title: Text("Error"),
                  message: Text("Cannot retrieve data"),
                  dismissButton: .default(Text("Ok")))
        }
    }
}

#if DEBUG
struct CarbonIntensityView_Previews: PreviewProvider {
    static var previews: some View {
        CarbonIntensityView()
    }
}
#endif

extension CarbonIntensity {
    
    
    
}
