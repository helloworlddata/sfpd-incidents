require 'pathname'

START_YEAR = 2003
END_YEAR = 2016

WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR.join('corral')
SCRIPTS_DIR = WRANGLE_DIR.join('scripts')

DIRS = {
    fetched: CORRAL_DIR.join('fetched'),
    cleaned: CORRAL_DIR.join('cleaned'),
    published: Pathname('data'),
}

FILES = {
    fetched: (START_YEAR..END_YEAR).map{|y| DIRS[:fetched].join("#{y}.csv")},
}



desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end


namespace :publish do
    desc "Fetch data from #{START_YEAR} through #{END_YEAR}"
    task :fetch do
        FILES[:fetched].each do |fn|
            Rake::Task[fn].execute()
        end
    end
end




FILES[:fetched].each do |fname|
    year = fname.to_s[/\d{4}(?=\.csv)/]
    file fname do
        sh "python #{SCRIPTS_DIR.join('fetch_year.py')} #{year} > #{fname}"
    end
end
