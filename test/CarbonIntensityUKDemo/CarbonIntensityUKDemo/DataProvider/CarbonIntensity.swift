//
//  CarbonIntensity.swift
//  DataProvider
//
//  Created by Mattia Campolese on 14/11/2020.
//

// https://carbon-intensity.github.io/api-definitions/#intensity-1
//{
//  "data":[
//    {
//    "from": "2018-01-20T12:00Z",
//    "to": "2018-01-20T12:30Z",
//    "intensity": {
//      "forecast": 266,
//      "actual": 263,
//      "index": "moderate"
//    }
//  }]
//}

import Foundation

struct CarbonIntensityWrapper: Codable {
    var data: [CarbonIntensity]
}

public struct CarbonIntensity: Codable {
    
    public struct Intensity: Codable {
        
        public enum IntensityIndex: String, Codable {
            case very_low = "very low"
            case low
            case moderate
            case high
            case very_high = "very high"
        }
        
        public var forecast: Int
        public var actual: Int
        public var index: IntensityIndex

    }
    
    public var from: Date
    public var to: Date
    public var intensity: Intensity

}
