//
//  CarbonIntensityService.swift
//  DataProvider
//
//  Created by Mattia Campolese on 14/11/2020.
//

import Foundation
import Alamofire

public struct CarbonIntensityService {
    
    private var host: String = "https://api.carbonintensity.org.uk"
    
    private var decoder: JSONDecoder
    
    public init() {
        let dateFormatter = DateFormatter()
        dateFormatter.locale = Locale(identifier: "en_US_POSIX")
        dateFormatter.dateFormat = "yyyy-MM-dd'T'HH:mmZ" //2018-01-20T12:00Z
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .formatted(dateFormatter)
        self.decoder = decoder
    }
    
    public func currentIntensity(completion: @escaping (Result<[CarbonIntensity], AFError>) -> Void) {
        AF.request("\(host)/intensity").responseDecodable(of: CarbonIntensityWrapper.self, decoder: decoder) { response in
            switch response.result {
            case .success(let values):
                completion(.success(values.data))
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }
    
}
