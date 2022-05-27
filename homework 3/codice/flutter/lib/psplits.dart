import 'package:flutter/cupertino.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'dart:convert';
import 'globals.dart';

import 'package:flutter/material.dart';


class Splits extends StatefulWidget {
  final atleta;
  final primo;
  const Splits (this.atleta, this.primo, {Key? key}) : super(key: key);
  static const routeName = '/Splits';

  @override
  State<Splits> createState() => SplitsState();
}

class SplitsState extends State<Splits> {
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return(
      Scaffold(
        appBar: AppBar(
          title: Text("Risultato atleta"),
        ),
        body:
          ListView(
            //tutto
            children: [
              Column(

                children: [
                  SizedBox(height: 10),
                  Text("${widget.atleta['family']} ${widget.atleta['given']}", textScaleFactor: name_surname_scale.toDouble()),
                  SizedBox(height: 10),
                  Text("CLUB: ${widget.atleta['club']['name']}"),
                  SizedBox(height: 10),
                  Text("POSIZIONE: ${widget.atleta['position']}"),
                  SizedBox(height: 10),
                  Text("TEMPO: ${widget.atleta['time']}"),
                ],
              ),
              Column(
                children: [
                  SizedBox(height: 20),
                  Text("Split Times:"),
                  
                  SizedBox(height: 10),
                  createSplitTable(widget.atleta, widget.primo)
                    ],
                  )
            ],
          )
      )
    );
  }
}

Widget createSplitTable(Map <String,dynamic> atleta, Map <String,dynamic> primo){

  List<DataRow> rows = [];
  int diff;
  int i = 0;


  for(var ciao in atleta['splits']){
      diff = ciao['time'] - primo['splits'][i]['time'];
      rows.add(DataRow(
        cells: <DataCell>[
          DataCell(Text(ciao['controlCode'].toString(), textAlign: TextAlign.center,)),
          DataCell(Text(ciao['time'].toString(), textAlign: TextAlign.center,)),
          DataCell(Text(diff.toString(), textAlign: TextAlign.center,))
        ])
      );
      
      i++;
    }
    return DataTable(
      columns: const <DataColumn>[
        DataColumn(
          label: Text(
            'INTERTEMPO',
            style: TextStyle(fontStyle: FontStyle.italic,),
            
          ),
        ),
        DataColumn(
          label: Text(
            'TEMPO',
            style: TextStyle(fontStyle: FontStyle.italic),
          ),
        ),
        DataColumn(
          label: Text(
            'DIFFERENZA',
            style: TextStyle(fontStyle: FontStyle.italic),
          ),
        ),
      ],

      rows: rows
    );
}