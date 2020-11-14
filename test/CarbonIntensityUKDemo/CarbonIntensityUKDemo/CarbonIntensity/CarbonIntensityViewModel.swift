//
//  CarbonIntensityViewModel.swift
//  CarbonIntensity
//
//  Created by Mattia Campolese on 14/11/2020.
//

import Combine
import Foundation
import DataProvider

final class CarbonIntensityViewModel: ObservableObject {
    
    @Published private(set) var carbonIntensity: CarbonIntensity? = nil
    @Published var showError: Bool = false
            
    private let service: CarbonIntensityService = CarbonIntensityService()
    
    func loadIntensities() {
        service.currentIntensity { [unowned self] result in
            switch result {
            case .success(let intensities):
                self.showError = false
                self.carbonIntensity = intensities.last
            case .failure:
                self.showError = true
            }
        }
    }
    
}
