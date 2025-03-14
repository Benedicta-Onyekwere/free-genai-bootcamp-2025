require 'httparty'
require 'json'

RSpec.describe 'Language Portal API' do
  let(:base_url) { 'http://localhost:3000/api' }

  describe 'Words API' do
    it 'lists words with pagination' do
      response = HTTParty.get("#{base_url}/words")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
      expect(json).to have_key('pagination')
      expect(json['pagination']).to include(
        'current_page',
        'total_pages',
        'total_items',
        'items_per_page'
      )
    end

    it 'gets a specific word' do
      # First get the list to find a valid ID
      list_response = HTTParty.get("#{base_url}/words")
      first_word = JSON.parse(list_response.body)['items'].first
      word_id = first_word['id']

      response = HTTParty.get("#{base_url}/words/#{word_id}")
      expect(response.code).to eq(200)
      
      word = JSON.parse(response.body)
      expect(word['id']).to eq(word_id)
      expect(word).to have_key('japanese')
      expect(word).to have_key('romaji')
      expect(word).to have_key('english')
    end
  end

  describe 'Groups API' do
    it 'lists groups with pagination' do
      response = HTTParty.get("#{base_url}/groups")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
      expect(json).to have_key('pagination')
    end

    it 'gets a specific group' do
      # First get the list to find a valid ID
      list_response = HTTParty.get("#{base_url}/groups")
      first_group = JSON.parse(list_response.body)['items'].first
      group_id = first_group['id']

      response = HTTParty.get("#{base_url}/groups/#{group_id}")
      expect(response.code).to eq(200)
      
      group = JSON.parse(response.body)
      expect(group['id']).to eq(group_id)
      expect(group).to have_key('name')
      expect(group).to have_key('word_count')
    end

    it 'lists words in a group' do
      # First get a valid group ID
      list_response = HTTParty.get("#{base_url}/groups")
      first_group = JSON.parse(list_response.body)['items'].first
      group_id = first_group['id']

      response = HTTParty.get("#{base_url}/groups/#{group_id}/words")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
      expect(json).to have_key('pagination')
    end

    it 'lists study sessions in a group' do
      # First get a valid group ID
      list_response = HTTParty.get("#{base_url}/groups")
      first_group = JSON.parse(list_response.body)['items'].first
      group_id = first_group['id']

      response = HTTParty.get("#{base_url}/groups/#{group_id}/study_sessions")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
      expect(json).to have_key('pagination')
    end
  end

  describe 'Study Activities API' do
    it 'lists study activities' do
      response = HTTParty.get("#{base_url}/study_activities")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
    end

    it 'gets a specific study activity' do
      # First get the list to find a valid ID
      list_response = HTTParty.get("#{base_url}/study_activities")
      first_activity = JSON.parse(list_response.body)['items'].first
      activity_id = first_activity['id']

      response = HTTParty.get("#{base_url}/study_activities/#{activity_id}")
      expect(response.code).to eq(200)
      
      activity = JSON.parse(response.body)
      expect(activity['id']).to eq(activity_id)
      expect(activity).to have_key('name')
      expect(activity).to have_key('description')
      expect(activity).to have_key('thumbnail_url')
    end

    it 'creates a new study activity' do
      response = HTTParty.post(
        "#{base_url}/study_activities",
        body: {
          name: 'Test Activity',
          description: 'Test Description',
          thumbnail_url: 'https://example.com/test.jpg'
        }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      )
      expect(response.code).to eq(201)
      
      activity = JSON.parse(response.body)
      expect(activity).to have_key('id')
      expect(activity['name']).to eq('Test Activity')
      expect(activity['description']).to eq('Test Description')
      expect(activity['thumbnail_url']).to eq('https://example.com/test.jpg')
    end
  end

  describe 'Study Sessions API' do
    it 'lists study sessions with pagination' do
      response = HTTParty.get("#{base_url}/study_sessions")
      expect(response.code).to eq(200)
      
      json = JSON.parse(response.body)
      expect(json).to have_key('items')
      expect(json).to have_key('pagination')
    end

    context 'when creating and using a study session' do
      let(:group_id) do
        response = HTTParty.get("#{base_url}/groups")
        JSON.parse(response.body)['items'].first['id']
      end

      let(:study_activity_id) do
        response = HTTParty.get("#{base_url}/study_activities")
        JSON.parse(response.body)['items'].first['id']
      end

      let(:study_session_id) do
        response = HTTParty.post(
          "#{base_url}/study_sessions",
          body: {
            group_id: group_id,
            study_activity_id: study_activity_id
          }.to_json,
          headers: { 'Content-Type' => 'application/json' }
        )
        
        expect(response.code).to eq(201)
        JSON.parse(response.body)['id']
      end

      it 'creates a new study session' do
        response = HTTParty.post(
          "#{base_url}/study_sessions",
          body: {
            group_id: group_id,
            study_activity_id: study_activity_id
          }.to_json,
          headers: { 'Content-Type' => 'application/json' }
        )
        expect(response.code).to eq(201)
        
        session = JSON.parse(response.body)
        expect(session['group_id']).to eq(group_id)
        expect(session['study_activity_id']).to eq(study_activity_id)
      end

      it 'gets a specific study session' do
        response = HTTParty.get("#{base_url}/study_sessions/#{study_session_id}")
        expect(response.code).to eq(200)
        
        session = JSON.parse(response.body)
        expect(session['id']).to eq(study_session_id)
      end

      it 'lists words in a study session' do
        response = HTTParty.get("#{base_url}/study_sessions/#{study_session_id}/words")
        expect(response.code).to eq(200)
        
        json = JSON.parse(response.body)
        expect(json).to have_key('items')
        expect(json).to have_key('pagination')
      end

      it 'adds a word review to a study session' do
        # First get a word from the group
        words_response = HTTParty.get("#{base_url}/groups/#{group_id}/words")
        expect(words_response.code).to eq(200)
        
        words = JSON.parse(words_response.body)['items']
        expect(words).not_to be_empty
        
        word_id = words.first['id']

        # Add a review
        response = HTTParty.post(
          "#{base_url}/study_sessions/#{study_session_id}/words/#{word_id}/review",
          body: { correct: true }.to_json,
          headers: { 'Content-Type' => 'application/json' }
        )
        expect(response.code).to eq(200)
        
        result = JSON.parse(response.body)
        expect(result['success']).to be true
        expect(result['word_id']).to eq(word_id)
        expect(result['study_session_id']).to eq(study_session_id)
        expect(result['correct']).to be true
      end
    end
  end

  describe 'Dashboard API' do
    it 'gets the last study session' do
      response = HTTParty.get("#{base_url}/dashboard/last_study_session")
      expect(response.code).to eq(200)
      
      data = JSON.parse(response.body)
      expect(data).to have_key('id')
      expect(data).to have_key('group_id')
      expect(data).to have_key('created_at')
      expect(data).to have_key('study_activity_id')
      expect(data).to have_key('group_name')
    end

    it 'gets study progress' do
      response = HTTParty.get("#{base_url}/dashboard/study_progress")
      expect(response.code).to eq(200)
      
      data = JSON.parse(response.body)
      expect(data).to have_key('total_words_studied')
      expect(data).to have_key('total_available_words')
    end

    it 'gets quick stats' do
      response = HTTParty.get("#{base_url}/dashboard/quick-stats")
      expect(response.code).to eq(200)
      
      data = JSON.parse(response.body)
      expect(data).to have_key('success_rate')
      expect(data).to have_key('total_study_sessions')
      expect(data).to have_key('total_active_groups')
      expect(data).to have_key('study_streak_days')
    end
  end
end 