import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './event.dart';



Future<List<Map<String, dynamic>>> fetchRaces() async {
  final response = await http.get(Uri.parse('$apiUrl/list_races'));

  if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
    return List<Map<String, dynamic>>.from(jsonDecode(response.body));
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load classes');
  }
}

void main() {
  runApp(const MaterialApp(
    title: 'Ori Live Results',
    home: EventsApp(),
  ));
}

class EventsApp extends StatefulWidget {
  const EventsApp({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _EventsAppState();
}

class _EventsAppState extends State<EventsApp> {

  late Future<List<Map<String, dynamic>>> futureEvents;

  @override
  void initState() {
    super.initState();
    futureEvents = fetchRaces();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Events'),
      ),
      body: Center(
        child: FutureBuilder<List<Map<String, dynamic>>> (
          future: futureEvents,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              var events = snapshot.data!;
              return RefreshIndicator(
                onRefresh: _pullRefresh,
                child: ListView.builder(
                  itemCount: events.length,
                  itemBuilder: ((context, index) => GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              EventApp(events[index]['ID'], events[index]['NomeGara']),
                        ),
                      );
                    },
                    child: Card(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                          ListTile(
                            title: Text(events[index]['NomeGara']),
                            subtitle: Text('Data: ' + events[index]['DataInizio']),
                          ),
                        ],
                      ),
                    )
                  ))
                )
              );
            } else if (snapshot.hasError){
              return Text('${snapshot.error}');
            }

            return const CircularProgressIndicator();
          } ,
        )
      ),
    );
  }

  Future<void> _pullRefresh() async {
    setState(() {
      futureEvents = fetchRaces();
    });
    await Future.delayed(Duration(seconds: 1));
  }
}

