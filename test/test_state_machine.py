from testix.frequentlyused import *
import pytest
from aots import state_machine

class TestStateMachine:
    def test_machine_starts_with_initial_state( self ):
        with Scenario() as scenario:
            scenario <<\
                Call( 'Idle' ).returns( FakeObject( 'idle' ) ) <<\
                Call( 'idle.enter', None, None )

            tested = state_machine.StateMachine( FakeObject( 'Idle' ) )
            assert tested.current is FakeObject( 'idle' )

    def switchStateScenario( self, scenario, currentStateClass, reason, nextStateClass ):
        currentStateInstance = currentStateClass.lower()
        nextStateInstance = nextStateClass.lower()
        scenario <<\
            Call( '{state}.next'.format( state = currentStateInstance ), reason ).returns( FakeObject( nextStateClass ) ) <<\
            Call( nextStateClass ).returns( FakeObject( nextStateInstance ) ) <<\
            Call( '{state}.enter'.format( state = nextStateInstance ), FakeObject( currentStateInstance ), reason )

    @pytest.fixture
    def idleMachine( self ):
        with Scenario() as scenario:
            scenario <<\
                Call( 'Idle' ).returns( FakeObject( 'idle' ) ) <<\
                Call( 'idle.enter', None, None )

            tested = state_machine.StateMachine( FakeObject( 'Idle' ) )
            assert tested.current is FakeObject( 'idle' )

        return tested

    def test_machine_goes_through_two_states( self, idleMachine ):
        tested = idleMachine

        with Scenario() as scenario:
            self.switchStateScenario( scenario, 'Idle', FakeObject( 'event' ), 'Starting' )
            tested.event( FakeObject( 'event' ) )
            assert tested.current is FakeObject( 'starting' )

    def test_event_ignored_state_stays_the_same( self, idleMachine ):
        tested = idleMachine

        with Scenario() as scenario:
            scenario <<\
                Call( 'idle.next', FakeObject( 'someEvent' ) ).returns( None )

            tested.event( FakeObject( 'someEvent' ) )
            assert tested.current is FakeObject( 'idle' )

    def test_machine_goes_through_some_states( self, idleMachine ):
        tested = idleMachine

        with Scenario() as scenario:
            self.switchStateScenario( scenario, 'Idle', FakeObject( 'start' ), 'Starting' )
            tested.event( FakeObject( 'start' ) )
            assert tested.current is FakeObject( 'starting' )

            self.switchStateScenario( scenario, 'Starting', FakeObject( 'play' ), 'Playing' )
            tested.event( FakeObject( 'play' ) )
            assert tested.current is FakeObject( 'playing' )

            self.switchStateScenario( scenario, 'Playing', FakeObject( 'stop' ), 'Stopping' )
            tested.event( FakeObject( 'stop' ) )
            assert tested.current is FakeObject( 'stopping' )

            self.switchStateScenario( scenario, 'Stopping', FakeObject( 'stopped' ), 'Idle' )
            tested.event( FakeObject( 'stopped' ) )
            assert tested.current is FakeObject( 'idle' )
