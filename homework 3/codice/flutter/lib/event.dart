import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import './clubs.dart';
import './categories.dart';

class EventApp extends StatefulWidget {
  final raceId;
  final nomeGara;
  const EventApp(this.raceId, this.nomeGara, {Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() => _EventAppState();

}

class _EventAppState extends State<EventApp> with TickerProviderStateMixin {

  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.nomeGara),
        bottom: TabBar(
          controller: _tabController,
          tabs: const <Widget>[
            Tab(
              icon: Text('Categorie'),
            ),
            Tab(
              icon: Text('Clubs'),
            ),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          Center(
            child: CategoriesList(widget.raceId),
          ),
          Center(
            child: ClubsList(widget.raceId),
          ),
        ],
      )
    );
  }
}
