class ScriptsController < ApplicationController
  before_action :authorize_admin
  def index
    render :dashboard
  end


  def authorize_admin
    unless current_user && current_user.role == 'admin'
      redirect_to root_path, alert: 'Access denied.'
    end
  end

  def run_script
    # Enqueue the script to be executed in the background immediately
    ScriptRunner.new.delay(run_at: 0.seconds.from_now).perform
    # Redirect to the index page to show the user that the script was enqueued
    system('rails jobs:work')
    redirect_to scripts_path
  end

  # Define a separate class to execute the script in the background
  class ScriptRunner < Struct.new(:controller, :args)
    def perform
      # Execute your Python script using the system method

      system("python #{Rails.root}/python/map_districts.py")
      Process.kill('INT', Process.pid)
    end
  end
end
  