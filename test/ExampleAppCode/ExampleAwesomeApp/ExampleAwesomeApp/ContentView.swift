//
//  ContentView.swift
//  ExampleAwesomeApp
//
//  Created by Mattia Campolese on 11/10/2020.
//

import SwiftUI
import InternalModule

struct ContentView: View {
    var body: some View {
        Text("Hello, world!")
            .padding()
        Assets.ambulance
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
