import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:flutter/src/painting/text_style.dart';
import 'package:flutter/src/material/list_tile.dart';

import './globals.dart';


Future<List<List<dynamic>>> fetchClubResults(String raceid, String clubid) async {
  final response = await http.get(Uri.parse('$apiUrl/results?id=$raceid&organization=$clubid'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    var val = List<dynamic>.from(jsonDecode(response.body));
    var classes = 0;
    var clubResults = [];
    var c = '';

    for (final res in val) {
      if (res['class'] != c) {
        classes++;
        clubResults.insert(classes - 1, []);
        c = res['class'];
      }
      clubResults[classes-1].add(res);
    }

    return List<List<dynamic>>.from(clubResults);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load clubs');
  }
}

class ClubResults extends StatefulWidget {
  final raceId;
  final clubId;
  final clubName;
  const ClubResults(this.raceId, this.clubId, this.clubName, {Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _ClubResultsState();

}

class _ClubResultsState extends State<ClubResults> {
  
  late Future<List<List<dynamic>>> futureClubResults;

  @override
  void initState() {
    super.initState();
    futureClubResults = fetchClubResults(widget.raceId, widget.clubId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Risultati Club ' + widget.clubName),
      ),
      body: Center(
        child: FutureBuilder<List<List<dynamic>>> (
          future: futureClubResults,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              
              var clubResults = snapshot.data!;

              return RefreshIndicator(
                onRefresh: _pullRefresh,
                child: ListView.builder(
                  itemCount: clubResults.length,
                  itemBuilder: ((context, index) => Column(
                    children: [
                      Card(
                        child: ListTile(title: Text(clubResults[index][0]['class']), dense: true, textColor: Colors.white,),
                        color: Color(0xFF90CAF9),
                      ),
                      ListView.builder(
                        physics: NeverScrollableScrollPhysics(),
                        shrinkWrap: true,
                        itemCount: clubResults[index].length,
                        itemBuilder: ((c, i) => Card(
                          child: ListTile(
                            title: Text(clubResults[index][i]['given'] + ' ' + clubResults[index][i]['family']),
                            subtitle: Text((clubResults[index][i]['position'] == -1) ? 'Non arrivato' : 'Tempo: ' + clubResults[index][i]['time'].toString() + ' sec - posizione: ' +  clubResults[index][i]['position'].toString()),
                          ),
                        )),
                      )
                    ],
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
      futureClubResults = fetchClubResults(widget.raceId, widget.clubId);
    });
    await Future.delayed(Duration(seconds: 1));
  }

}
