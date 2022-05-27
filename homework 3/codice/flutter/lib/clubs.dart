import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './clubResults.dart';

Future<List<Map<String, dynamic>>> fetchClubs(String raceid) async {
  final response = await http.get(Uri.parse('$apiUrl/list_organizations?id=$raceid'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    if (response.body == '') {
      return List<Map<String, dynamic>>.empty();
    }
    return List<Map<String, dynamic>>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load clubs');
  }
}

class ClubsList extends StatefulWidget {
  final raceId;
  const ClubsList(this.raceId, {Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _ClubsListState();

}

class _ClubsListState extends State<ClubsList> {

  late Future<List<Map<String, dynamic>>> futureClubs;

  @override
  void initState() {
    super.initState();
    futureClubs = fetchClubs(widget.raceId);
  }
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>> (
      future: futureClubs,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          var clubs = snapshot.data!;
          return RefreshIndicator(
            onRefresh: _pullRefresh,
            child: ListView.builder(
              itemCount: clubs.length,
              itemBuilder: ((context, index) => GestureDetector(
                onTap: () {
                  Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              ClubResults(widget.raceId, clubs[index]['id'], clubs[index]['name']),
                        ),
                      );
                },
                child: Card(
                  child: ListTile(title: Text(clubs[index]['name']))
                ),
              ))
            )
          );
        } else if (snapshot.hasError){
          return Text('${snapshot.error}');
        }

        return const CircularProgressIndicator();
      },
    );
  }

  Future<void> _pullRefresh() async {
    setState(() {
      futureClubs = fetchClubs(widget.raceId);
    });
    await Future.delayed(Duration(seconds: 1));
  }

}