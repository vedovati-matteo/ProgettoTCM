import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import './globals.dart';
import './categoriesResults.dart';

Future<List<Map<String, dynamic>>> fetchCategories(String raceid) async {
  final response = await http.get(Uri.parse('$apiUrl/list_classes?id=$raceid'));

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
    throw Exception('Failed to load categories');
  }
}

class CategoriesList extends StatefulWidget {
  final raceId;
  const CategoriesList(this.raceId, {Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _CategoriesListState();

}

class _CategoriesListState extends State<CategoriesList> {

  late Future<List<Map<String, dynamic>>> futureCategories;

  @override
  void initState() {
    super.initState();
    futureCategories = fetchCategories(widget.raceId);
  }
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>> (
      future: futureCategories,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          var classes = snapshot.data!;
          return RefreshIndicator(
            onRefresh: _pullRefresh,
            child: ListView.builder(
              itemCount: classes.length,
              itemBuilder: ((context, index) => GestureDetector(
                onTap: () {
                  Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              CategoryResults(widget.raceId, classes[index]['id'], classes[index]['class']),
                        ),
                      );
                },
                child: Card(
                  child: ListTile(title: Text(classes[index]['class']))
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
      futureCategories = fetchCategories(widget.raceId);
    });
    await Future.delayed(Duration(seconds: 1));
  }

}