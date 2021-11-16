<?php

namespace JutiaDev\Category\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

class RefreshMigrationCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'migrate_category:refresh';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'refresh category migrations';

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $basePath = 'package/category';

        Artisan::call(
            'migrate:refresh',
            [
                '--path' => "$basePath/database/migrations/2021_11_13_000001_create_categorizable_table.php",
            ]
        );

        Artisan::call(
            'migrate:refresh',
            [
                '--path' => "$basePath/database/migrations/2021_11_13_000002_add_categories_foreign_key_to_related_models.php",
            ]
        );

        return true;
    }
}
