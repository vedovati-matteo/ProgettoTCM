import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:flutter/src/painting/text_style.dart';
import 'package:flutter/src/material/list_tile.dart';

import './globals.dart';
import 'psplits.dart';


Future<List<Map<String, dynamic>>> fetchCategorieResults(String raceid, String classid) async {
  final response = await http.get(Uri.parse('$apiUrl/results?id=$raceid&class=$classid'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    var val = List<Map<String, dynamic>>.from(jsonDecode(response.body));
    List<Map<String, dynamic>> finito = [];
    List<Map<String, dynamic>> nonFinito = [];
    val.forEach((element) {
      if (element['position'] == -1) {
        nonFinito.add(element);
      } else {
        finito.add(element);
      }
    });
    finito.addAll(nonFinito);
    return finito;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load category results');
  }
}

class CategoryResults extends StatefulWidget {
  final raceId;
  final classId;
  final className;
  const CategoryResults(this.raceId, this.classId, this.className, {Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _CategoryResultsState();

}

class _CategoryResultsState extends State<CategoryResults> {
  
  late Future<List<Map<String, dynamic>>> futureClassResults;

  @override
  void initState() {
    super.initState();
    futureClassResults = fetchCategorieResults(widget.raceId, widget.classId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Risultati Club ' + widget.className),
      ),
      body: Center(
        child: FutureBuilder<List<Map<String, dynamic>>> (
          future: futureClassResults,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              
              var classResults = snapshot.data!;

              return RefreshIndicator(
                onRefresh: _pullRefresh,
                child: ListView.builder(
                  itemCount: classResults.length,
                  itemBuilder: ((context, index) => GestureDetector(
                    onTap: () {
                      if (classResults[0]['position'] == 1 && classResults[index]['position'] != -1) {
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                Splits(classResults[index], classResults[0])
                            ),
                          );
                      }
                      
                    },
                    child: Card(
                        child: ListTile(
                            title: Text(classResults[index]['given'] + ' ' + classResults[index]['family']),
                            subtitle: Text((classResults[index]['position'] == -1) ? 'Non arrivato' : 'Posizione: ' +  classResults[index]['position'].toString() + ' - Tempo: ' + classResults[index]['time'].toString() + ' sec'),
                          )
                      )
                  ))
                )
              );
            } else if (snapshot.hasError){
              return Text('${snapshot.error}');
            }

            return const CircularProgressIndicator();
          },
        )
      )
    );
  }

  Future<void> _pullRefresh() async {
    setState(() {
      futureClassResults = fetchCategorieResults(widget.raceId, widget.classId);
    });
    await Future.delayed(Duration(seconds: 1));
  }

}
